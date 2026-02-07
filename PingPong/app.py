from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpingpong!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game state
# games[room_code] = {
#    'players': {sid1: 'left', sid2: 'right'},
#    'scores': {'left': 0, 'right': 0},
#    'ball': {'x': 400, 'y': 300, 'vx': 5, 'vy': 3},
#    'paddles': {'left': 250, 'right': 250},
#    'game_started': False
# }
games = {}

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def create_game():
    room = generate_code()
    
    games[room] = {
        'players': {request.sid: 'left'},
        'scores': {'left': 0, 'right': 0},
        'ball': {'x': 400, 'y': 300, 'vx': 5, 'vy': 3},
        'paddles': {'left': 250, 'right': 250},
        'game_started': False
    }
    
    join_room(room)
    emit('game_created', {
        'room': room,
        'side': 'left'
    })

@socketio.on('join_game')
def join_game(data):
    room = data['room'].upper()
    
    if room not in games:
        emit('error', {'message': 'Room not found'})
        return
    
    game = games[room]
    
    if len(game['players']) >= 2:
        emit('error', {'message': 'Room is full'})
        return
    
    game['players'][request.sid] = 'right'
    join_room(room)
    
    emit('game_joined', {
        'room': room,
        'side': 'right'
    })
    
    # Notify both players that game can start
    game['game_started'] = True
    emit('game_ready', {}, to=room)

@socketio.on('paddle_move')
def paddle_move(data):
    room = data['room']
    y = data['y']
    
    if room in games:
        game = games[room]
        side = game['players'].get(request.sid)
        if side:
            game['paddles'][side] = y
            # Broadcast paddle position to other player
            emit('opponent_paddle', {'side': side, 'y': y}, to=room, include_self=False)

@socketio.on('ball_update')
def ball_update(data):
    """Only the left player (host) sends ball updates"""
    room = data['room']
    
    if room in games:
        game = games[room]
        
        # Only accept ball updates from the left player
        if game['players'].get(request.sid) == 'left':
            game['ball'] = data['ball']
            # Broadcast to right player
            emit('ball_sync', {'ball': data['ball']}, to=room, include_self=False)

@socketio.on('score_update')
def score_update(data):
    """Only the left player (host) sends score updates"""
    room = data['room']
    
    if room in games:
        game = games[room]
        
        # Only accept score updates from the left player
        if game['players'].get(request.sid) == 'left':
            game['scores'] = data['scores']
            game['ball'] = data['ball']
            # Broadcast to right player
            emit('score_sync', {
                'scores': data['scores'],
                'ball': data['ball']
            }, to=room)

@socketio.on('reset_game')
def reset_game(data):
    room = data['room']
    
    if room in games:
        game = games[room]
        game['scores'] = {'left': 0, 'right': 0}
        game['ball'] = {'x': 400, 'y': 300, 'vx': 5, 'vy': 3}
        
        emit('game_reset', {
            'scores': game['scores'],
            'ball': game['ball']
        }, to=room)

@socketio.on('disconnect')
def disconnect():
    # Find and clean up games where this player was
    for room, game in list(games.items()):
        if request.sid in game['players']:
            emit('opponent_left', {}, to=room, include_self=False)
            del games[room]
            break

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5002, host='0.0.0.0')
