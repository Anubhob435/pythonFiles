# ConnectPro - WebRTC Communication App

A secure peer-to-peer video calling, audio calling, and text messaging application built with Python and WebRTC.

![ConnectPro](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![WebRTC](https://img.shields.io/badge/WebRTC-Enabled-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## ✨ Features

- 🎥 **HD Video Calls** - Crystal clear peer-to-peer video
- 🎤 **Crystal Audio** - High-quality audio with echo cancellation
- 💬 **Instant Chat** - Real-time text messaging during calls
- 🔒 **Secure** - HTTPS + JWT authentication
- 🎨 **Modern UI** - Dark glassmorphism design
- 📱 **Responsive** - Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd d:\Adams-call
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   uv venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   
   uv pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python -m server.main
   ```

4. **Open in browser:**
   ```
   https://localhost:8443
   ```
   
   > ⚠️ Accept the self-signed certificate warning in your browser

## 📖 Usage

1. **Create an Account** - Register with a username and password
2. **Create or Join Room** - Start a new room or enter a room code to join
3. **Share Room Code** - Give the 6-character code to others to join
4. **Start Calling** - Video, audio, and chat are ready to use!

## 🎮 Call Controls

| Button | Action |
|--------|--------|
| 🎤 | Toggle microphone on/off |
| 📹 | Toggle camera on/off |
| 💬 | Open/close chat panel |
| 📋 | Copy room code to clipboard |
| 📞 | End call and return to lobby |

## 🏗️ Project Structure

```
Adams-call/
├── server/
│   ├── main.py          # HTTPS server entry point
│   ├── signaling.py     # WebSocket signaling
│   ├── auth.py          # JWT authentication
│   └── rooms.py         # Room management
├── static/
│   ├── index.html       # Main UI
│   ├── css/styles.css   # Styling
│   └── js/
│       ├── app.js       # Application logic
│       ├── webrtc.js    # WebRTC client
│       └── chat.js      # Chat functionality
├── certs/               # SSL certificates (generated)
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

Environment variables (optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8443` | Server port |
| `JWT_SECRET_KEY` | Auto-generated | JWT signing key |

## 🛡️ Security

- **HTTPS** - All traffic is encrypted with TLS
- **JWT Tokens** - Secure authentication
- **Bcrypt** - Password hashing
- **WebRTC** - Peer-to-peer encrypted media

## 📝 License

MIT License - Feel free to use and modify!

---

Made with ❤️ using Python, aiortc, and modern web technologies
