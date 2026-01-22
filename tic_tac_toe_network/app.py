from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game state storage
# games[room_id] = {
#     'board': [''] * 9,
#     'turn': 'X',
#     'players': 0
# }
games = {}

def generate_room_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        if code not in games:
            return code

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def create_game():
    room = generate_room_code()
    games[room] = {
        'board': [''] * 9,
        'turn': 'X',
        'players': 1
    }
    join_room(room)
    emit('game_created', {'room': room})
    print(f"Game created: {room}")

@socketio.on('join_game')
def join_game(data):
    room = data['room']
    if room in games:
        if games[room]['players'] < 2:
            games[room]['players'] += 1
            join_room(room)
            emit('game_joined', {'room': room})
            emit('player_joined', to=room)
            print(f"Player joined game: {room}")
        else:
            emit('error', 'Room is full')
    else:
        emit('error', 'Room not found')

@socketio.on('make_move')
def make_move(data):
    room = data['room']
    index = int(data['index'])
    
    if room in games:
        game = games[room]
        # Check if it's the correct turn and cell is empty
        # We don't have player identification in this simple version effectively, 
        # relying on client side 'myTurn' logic mostly, but we should enforce 'turn' on server
        # For simplicity in this "play with friend" setup, strict session-to-player mapping 
        # isn't implemented (would require session IDs), but we trust the flow.
        
        if game['board'][index] == '':
            symbol = game['turn']
            game['board'][index] = symbol
            
            # Check win/draw
            winner = check_winner(game['board'])
            is_draw = '' not in game['board'] and not winner
            
            game_over = bool(winner or is_draw)
            result = winner if winner else ('draw' if is_draw else None)
            
            # Switch turn
            next_turn = 'O' if symbol == 'X' else 'X'
            game['turn'] = next_turn
            
            emit('move_made', {
                'index': index,
                'symbol': symbol,
                'next_turn': next_turn,
                'game_over': game_over,
                'result': result
            }, to=room)

@socketio.on('restart_game')
def restart_game(data):
    room = data['room']
    if room in games:
        games[room]['board'] = [''] * 9
        games[room]['turn'] = 'X'
        emit('game_restarted', to=room)

def check_winner(board):
    winning_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    
    for a, b, c in winning_combos:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
