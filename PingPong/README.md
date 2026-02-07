# 🏓 Multiplayer Ping Pong Game

A real-time multiplayer ping pong game built with Flask-SocketIO. Create or join rooms to play with friends!

## Features

- **Room-based multiplayer**: Create a game and share the room code with a friend
- **Real-time gameplay**: Smooth paddle and ball synchronization using WebSockets
- **Score tracking**: First to 5 points wins
- **Increasing difficulty**: Ball speed increases with each paddle hit
- **Simple controls**: Use arrow keys to move your paddle
- **Minimalist design**: Clean black and white UI with retro styling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5002
```

3. Create a game or join an existing room with a 4-character code

## How to Play

1. **Create a Game**: Click "Create Game" to start a new room. Share the room code with your friend.
2. **Join a Game**: Enter the 4-character room code and click "Join Game".
3. **Controls**: Use ↑ and ↓ arrow keys to move your paddle.
4. **Win**: First player to reach 5 points wins!
5. **Challenge**: Ball speed increases with each hit - keep up!

## Technical Details

- **Backend**: Flask + Flask-SocketIO for real-time communication
- **Frontend**: Vanilla JavaScript with HTML5 Canvas
- **Port**: Runs on port 5002 by default
- **Game Logic**: Left player (host) handles ball physics and collision detection

## Game Mechanics
by 0.15 units with each paddle hit
- Ball speed resets to 5 when a point is scored
- Paddles are highlighted in green (yours)
- Random ball trajectory on serve
- Reset game option to play multiple rounds
- First to 5 points wins the match
- Reset game option to play multiple rounds
