# Tic-Tac-Toe Network Game

A real-time multiplayer Tic-Tac-Toe game built with Flask and Socket.IO. Play the classic game with friends on your local network.

## Features

- 🎮 **Real-time Multiplayer**: Play with a friend over your local network
- 🎯 **Classic Gameplay**: Traditional 3x3 Tic-Tac-Toe rules
- 🎨 **Minimalist UI**: Clean black and white boxy design
- 🔄 **Replay Option**: Play again with the same opponent
- 📊 **Live Updates**: Board updates in real-time for both players
- ✨ **Visual Feedback**: Different colors for X (blue) and O (red)

## Screenshots

The game features a minimalist black background with white borders, creating a clean and modern aesthetic. X's appear in blue and O's in red for easy distinction.

## Installation

### Prerequisites

- Python 3.7+
- `uv` package manager (recommended) or `pip`

### Setup

1. **Navigate to the project directory**:
   ```bash
   cd tic_tac_toe_network
   ```

2. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```

   Or using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Usage

1. **Start the server**:
   ```bash
   uv run app.py
   ```

2. **Access the game**:
   - Open your browser to `http://localhost:5000`
   - For network play, use `http://<your-ip-address>:5000`

3. **Create a game**:
   - Click "Create Room"
   - Share the room code with your friend

4. **Join a game**:
   - Enter the room code
   - Click "Join Room"

5. **Play**:
   - Player 1 (creator) is **X** and goes first
   - Player 2 (joiner) is **O**
   - Click on any empty cell to make your move
   - The game announces the winner or draw
   - Click "Play Again" to restart

## Game Rules

- Players take turns placing their symbol (X or O) on the 3x3 grid
- First player to get 3 in a row (horizontally, vertically, or diagonally) wins
- If all 9 cells are filled without a winner, the game is a draw

### Winning Combinations

- **Rows**: Three in a row horizontally
- **Columns**: Three in a row vertically
- **Diagonals**: Three in a row diagonally

## Technical Stack

- **Backend**: Flask, Flask-SocketIO, Eventlet
- **Frontend**: Vanilla JavaScript, Socket.IO Client
- **Styling**: Pure CSS with custom design

## Project Structure

```
tic_tac_toe_network/
├── app.py                 # Flask server and game logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Styling
    └── game.js           # Client-side game logic
```

## Configuration

The server runs on port `5000` by default. To change this, edit `app.py`:

```python
socketio.run(app, debug=True, port=YOUR_PORT, host='0.0.0.0')
```

## Troubleshooting

### Port Already in Use

If you see an error about port 5000 being in use:

1. Find the process using the port:
   ```bash
   netstat -ano | findstr :5000
   ```

2. Kill the process:
   ```bash
   taskkill /PID <process_id> /F
   ```

### Connection Issues

- Ensure both players are on the same network
- Check firewall settings allow connections on port 5000
- Verify the server is running before joining

### Game Not Starting

- Make sure both players have joined the room
- Refresh the page if the game doesn't start automatically
- Check the browser console for any error messages

## License

This project is open source and available for personal and educational use.

## Author

Created as part of a network gaming project series.
