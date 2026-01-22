from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit, leave_room
import random
import string
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretrps!'
socketio = SocketIO(app, cors_allowed_origins="*")

# State
# games[room_code] = {
#    'rounds_total': 3,
#    'rounds_needed': 2,
#    'current_round': 1,
#    'players': [sid1, sid2], 
#    'scores': {sid1: 0, sid2: 0},
#    'moves': {}, # {sid1: 'rock'}
# }
games = {}

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def create_game(data):
    rounds = int(data.get('rounds', 3))
    room = generate_code()
    
    games[room] = {
        'rounds_total': rounds,
        'rounds_needed': math.ceil(rounds / 2),
        'current_round': 1,
        'players': [request.sid],
        'scores': {request.sid: 0},
        'moves': {}
    }
    
    join_room(room)
    emit('game_created', {'room': room, 'total_rounds': rounds})

@socketio.on('join_game')
def join_game(data):
    room = data['room']
    if room in games:
        game = games[room]
        if len(game['players']) < 2:
            game['players'].append(request.sid)
            game['scores'][request.sid] = 0
            join_room(room)
            
            # Notify joiner
            emit('game_joined', {'room': room, 'current_round': game['current_round'], 'total_rounds': game['rounds_total']})
            
            # Start Round 1
            emit('start_round', {'round': 1, 'total_rounds': game['rounds_total']}, to=room)
        else:
            emit('error', 'Room is full')
    else:
        emit('error', 'Room not found')

@socketio.on('make_move')
def make_move(data):
    room = data['room']
    move = data['move']
    sid = request.sid
    
    if room in games:
        game = games[room]
        # Store move
        game['moves'][sid] = move
        
        # Check if both moved
        if len(game['moves']) == 2:
            evaluate_round(room)

def evaluate_round(room):
    game = games[room]
    p1 = game['players'][0]
    p2 = game['players'][1]
    
    m1 = game['moves'][p1]
    m2 = game['moves'][p2]
    
    winner = None # None = draw, p1, p2
    
    if m1 == m2:
        winner = None
    elif (m1 == 'rock' and m2 == 'scissors') or \
         (m1 == 'paper' and m2 == 'rock') or \
         (m1 == 'scissors' and m2 == 'paper'):
        winner = p1
        game['scores'][p1] += 1
    else:
        winner = p2
        game['scores'][p2] += 1
        
    # Send results to each player
    emit('round_result', {
        'result': 'win' if winner == p1 else ('loss' if winner == p2 else 'draw'),
        'opp_move': m2,
        'new_scores': {'you': game['scores'][p1], 'opp': game['scores'][p2]},
        'game_over': False # temporary, fixed below
    }, to=p1)
    
    emit('round_result', {
        'result': 'win' if winner == p2 else ('loss' if winner == p1 else 'draw'),
        'opp_move': m1,
        'new_scores': {'you': game['scores'][p2], 'opp': game['scores'][p1]},
        'game_over': False
    }, to=p2)
    
    # Check Game Over
    check_game_over(room, winner)

def check_game_over(room, round_winner):
    game = games[room]
    p1 = game['players'][0]
    p2 = game['players'][1]
    
    s1 = game['scores'][p1]
    s2 = game['scores'][p2]
    needed = game['rounds_needed']
    current_round = game['current_round']
    total_rounds = game['rounds_total']
    
    game_winner = None
    is_draw = False
    
    # Check if someone won the majority
    if s1 >= needed:
        game_winner = p1
    elif s2 >= needed:
        game_winner = p2
    # Check if all rounds are complete
    elif current_round >= total_rounds:
        # All rounds played, determine winner by score
        if s1 > s2:
            game_winner = p1
        elif s2 > s1:
            game_winner = p2
        else:
            is_draw = True
    
    # If game is over (win or draw)
    if game_winner or is_draw:
        if is_draw:
            emit('game_over', {'winner': 'draw'}, to=p1)
            emit('game_over', {'winner': 'draw'}, to=p2)
        else:
            emit('game_over', {'winner': 'you' if game_winner == p1 else 'opp'}, to=p1)
            emit('game_over', {'winner': 'you' if game_winner == p2 else 'opp'}, to=p2)
    else:
        # Reset moves, increment round
        game['moves'] = {}
        game['current_round'] += 1
        
        # Adding a small delay is handled by client, server ready for input
        socketio.sleep(2) # Allow clients to see result
        emit('start_round', {'round': game['current_round'], 'total_rounds': game['rounds_total']}, to=room)


@socketio.on('restart_game')
def restart_game(data):
    room = data['room']
    if room in games:
        game = games[room]
        # Reset scores and round
        game['current_round'] = 1
        game['moves'] = {}
        for pid in game['players']:
            game['scores'][pid] = 0
            
        emit('game_restarted', {'total_rounds': game['rounds_total']}, to=room)
        socketio.sleep(0.5)
        emit('start_round', {'round': 1, 'total_rounds': game['rounds_total']}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001, host='0.0.0.0')
