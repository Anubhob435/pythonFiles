# Rock-Paper-Scissors Network Game

A real-time multiplayer Rock-Paper-Scissors game built with Flask and Socket.IO. Play with friends on your local network with customizable round options.

## Features

- 🎮 **Real-time Multiplayer**: Play with a friend over your local network
- 🎯 **Best-of-N Rounds**: Choose between 3, 5, or 7 rounds
- 🏆 **Smart Win Detection**: Game ends when someone wins the majority OR after all rounds complete
- 🎨 **Minimalist UI**: Clean black and white boxy design
- 🔄 **Replay Option**: Play again with the same opponent
- 📊 **Live Score Tracking**: Scores update after each round

## Screenshots

The game features a minimalist black background with white borders and text, creating a retro terminal-like aesthetic.

## Installation

### Prerequisites

- Python 3.7+
- `uv` package manager (recommended) or `pip`

### Setup

1. **Navigate to the project directory**:
   ```bash
   cd rock_paper_scissors
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
   - Open your browser to `http://localhost:5001`
   - For network play, use `http://<your-ip-address>:5001`

3. **Create a game**:
   - Select the number of rounds (3, 5, or 7)
   - Click "Create Room"
   - Share the room code with your friend

4. **Join a game**:
   - Enter the room code
   - Click "Join Room"

5. **Play**:
   - Both players select Rock, Paper, or Scissors
   - Results are revealed when both players have made their choice
   - First to win the majority of rounds wins the game
   - If all rounds complete without a majority, the player with more wins takes the game

## Game Rules

- **Rock** beats **Scissors**
- **Scissors** beats **Paper**
- **Paper** beats **Rock**
- **Draw**: Both players pick the same move

### Winning Conditions

- **Best of 3**: First to 2 wins
- **Best of 5**: First to 3 wins
- **Best of 7**: First to 4 wins
- **Draw**: If all rounds complete and scores are tied

## Technical Stack

- **Backend**: Flask, Flask-SocketIO, Eventlet
- **Frontend**: Vanilla JavaScript, Socket.IO Client
- **Styling**: Pure CSS with custom design

## Project Structure

```
rock_paper_scissors/
├── app.py                 # Flask server and game logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # Styling
    └── game.js           # Client-side game logic
```

## Configuration

The server runs on port `5001` by default. To change this, edit `app.py`:

```python
socketio.run(app, debug=True, port=YOUR_PORT, host='0.0.0.0')
```

## Troubleshooting

### Port Already in Use

If you see an error about port 5001 being in use:

1. Find the process using the port:
   ```bash
   netstat -ano | findstr :5001
   ```

2. Kill the process:
   ```bash
   taskkill /PID <process_id> /F
   ```

### Connection Issues

- Ensure both players are on the same network
- Check firewall settings allow connections on port 5001
- Verify the server is running before joining

## License

This project is open source and available for personal and educational use.

## Author

Created as part of a network gaming project series.
