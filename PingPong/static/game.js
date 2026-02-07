const socket = io();

// DOM elements
const menuScreen = document.getElementById('menu');
const gameScreen = document.getElementById('game');
const createBtn = document.getElementById('createBtn');
const joinBtn = document.getElementById('joinBtn');
const roomInput = document.getElementById('roomInput');
const roomCodeDiv = document.getElementById('roomCode');
const roomCodeText = document.getElementById('roomCodeText');
const currentRoomText = document.getElementById('currentRoom');
const status = document.getElementById('status');
const scoreDisplay = document.getElementById('scoreDisplay');
const resetBtn = document.getElementById('resetBtn');
const leaveBtn = document.getElementById('leaveBtn');

// Canvas setup
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let currentRoom = null;
let mySide = null;
let gameReady = false;

// Game objects
const PADDLE_WIDTH = 10;
const PADDLE_HEIGHT = 100;
const BALL_SIZE = 10;
const WINNING_SCORE = 5;
const SPEED_INCREASE = 0.15; // Speed increase per hit

let ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    vx: 5,
    vy: 3,
    speed: 5
};

let paddles = {
    left: canvas.height / 2 - PADDLE_HEIGHT / 2,
    right: canvas.height / 2 - PADDLE_HEIGHT / 2
};

let scores = {
    left: 0,
    right: 0
};

let keys = {};

// Event listeners
createBtn.addEventListener('click', () => {
    socket.emit('create_game');
});

joinBtn.addEventListener('click', () => {
    const room = roomInput.value.trim().toUpperCase();
    if (room.length === 4) {
        socket.emit('join_game', { room });
    } else {
        setStatus('Please enter a 4-character room code');
    }
});

resetBtn.addEventListener('click', () => {
    socket.emit('reset_game', { room: currentRoom });
});

leaveBtn.addEventListener('click', () => {
    location.reload();
});

document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Socket events
socket.on('game_created', (data) => {
    currentRoom = data.room;
    mySide = data.side;
    roomCodeText.textContent = data.room;
    roomCodeDiv.classList.remove('hidden');
    setStatus('Waiting for opponent...');
});

socket.on('game_joined', (data) => {
    currentRoom = data.room;
    mySide = data.side;
    setStatus('Joined! Waiting for game to start...');
});

socket.on('game_ready', () => {
    gameReady = true;
    showGameScreen();
    setStatus('');
    startGame();
});

socket.on('opponent_paddle', (data) => {
    paddles[data.side] = data.y;
});

socket.on('ball_sync', (data) => {
    // Right player receives ball position from left player
    ball = data.ball;
});

socket.on('score_sync', (data) => {
    scores = data.scores;
    ball = data.ball;
    updateScoreDisplay();
    checkWinner();
});

socket.on('game_reset', (data) => {
    scores = data.scores;
    ball = data.ball;
    updateScoreDisplay();
});

socket.on('opponent_left', () => {
    alert('Opponent left the game');
    location.reload();
});

socket.on('error', (data) => {
    setStatus(data.message || 'An error occurred');
});

// Helper functions
function setStatus(msg) {
    status.textContent = msg;
}

function showGameScreen() {
    menuScreen.classList.add('hidden');
    gameScreen.classList.remove('hidden');
    currentRoomText.textContent = currentRoom;
}

function updateScoreDisplay() {
    scoreDisplay.textContent = `${scores.left} - ${scores.right}`;
}

function checkWinner() {
    if (scores.left >= WINNING_SCORE) {
        setTimeout(() => {
            alert(mySide === 'left' ? 'You Win! 🎉' : 'Opponent Wins!');
        }, 100);
    } else if (scores.right >= WINNING_SCORE) {
        setTimeout(() => {
            alert(mySide === 'right' ? 'You Win! 🎉' : 'Opponent Wins!');
        }, 100);
    }
}

// Game loop
function startGame() {
    gameLoop();
}

function gameLoop() {
    if (!gameReady) return;

    // Handle paddle movement
    const myPaddleY = paddles[mySide];
    let newY = myPaddleY;

    if (keys['ArrowUp'] && myPaddleY > 0) {
        newY = myPaddleY - 8;
    }
    if (keys['ArrowDown'] && myPaddleY < canvas.height - PADDLE_HEIGHT) {
        newY = myPaddleY + 8;
    }

    if (newY !== myPaddleY) {
        paddles[mySide] = newY;
        socket.emit('paddle_move', {
            room: currentRoom,
            y: newY
        });
    }

    // Only left player updates ball physics
    if (mySide === 'left') {
        updateBall();
    }

    // Render
    draw();

    requestAnimationFrame(gameLoop);
}

function updateBall() {
    ball.x += ball.vx;
    ball.y += ball.vy;

    // Top and bottom collision
    if (ball.y <= 0 || ball.y >= canvas.height - BALL_SIZE) {
        ball.vy *= -1;
    }

    // Left paddle collision
    if (ball.x <= PADDLE_WIDTH + BALL_SIZE &&
        ball.y >= paddles.left &&
        ball.y <= paddles.left + PADDLE_HEIGHT) {
        ball.vx = Math.abs(ball.vx);
        ball.vy += (Math.random() - 0.5) * 2;
        // Increase speed on hit
        ball.speed += SPEED_INCREASE;
        ball.vx = (ball.vx / Math.abs(ball.vx)) * ball.speed;
    }

    // Right paddle collision
    if (ball.x >= canvas.width - PADDLE_WIDTH - BALL_SIZE * 2 &&
        ball.y >= paddles.right &&
        ball.y <= paddles.right + PADDLE_HEIGHT) {
        ball.vx = -Math.abs(ball.vx);
        ball.vy += (Math.random() - 0.5) * 2;
        // Increase speed on hit
        ball.speed += SPEED_INCREASE;
        ball.vx = (ball.vx / Math.abs(ball.vx)) * ball.speed;
    }

    // Score points
    if (ball.x < 0) {
        scores.right++;
        resetBall();
        socket.emit('score_update', {
            room: currentRoom,
            scores: scores,
            ball: ball
        });
        updateScoreDisplay();
        checkWinner();
    } else if (ball.x > canvas.width) {
        scores.left++;
        resetBall();
        socket.emit('score_update', {
            room: currentRoom,
            scores: scores,
            ball: ball
        });
        updateScoreDisplay();
        checkWinner();
    }

    // Send ball update to opponent
    socket.emit('ball_update', {
        room: currentRoom,
        ball: ball
    });speed = 5; // Reset speed
    ball.
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.vx = (Math.random() > 0.5 ? 1 : -1) * 5;
    ball.vy = (Math.random() - 0.5) * 6;
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw center line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw paddles
    ctx.fillStyle = '#fff';
    // Left paddle
    ctx.fillRect(0, paddles.left, PADDLE_WIDTH, PADDLE_HEIGHT);
    // Right paddle
    ctx.fillRect(canvas.width - PADDLE_WIDTH, paddles.right, PADDLE_WIDTH, PADDLE_HEIGHT);

    // Draw ball
    ctx.fillStyle = '#fff';
    ctx.fillRect(ball.x, ball.y, BALL_SIZE, BALL_SIZE);

    // Highlight my paddle
    if (mySide === 'left') {
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(0, paddles.left, PADDLE_WIDTH, PADDLE_HEIGHT);
    } else {
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        ctx.strokeRect(canvas.width - PADDLE_WIDTH, paddles.right, PADDLE_WIDTH, PADDLE_HEIGHT);
    }
}
