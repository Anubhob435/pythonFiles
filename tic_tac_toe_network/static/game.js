const socket = io();

// DOM Elements
const landingPage = document.getElementById('landing-page');
const gameRoom = document.getElementById('game-room');
const btnCreate = document.getElementById('btn-create');
const btnJoin = document.getElementById('btn-join');
const roomInput = document.getElementById('room-code-input');
const displayRoomCode = document.getElementById('display-room-code');
const playerStatus = document.getElementById('player-status');
const cells = document.querySelectorAll('.cell');
const gameResult = document.getElementById('game-result');
const resultMessage = document.getElementById('result-message');
const btnReplay = document.getElementById('btn-replay');

let currentRoom = null;
let mySymbol = null;
let isMyTurn = false;

// Event Listeners
btnCreate.addEventListener('click', () => {
    socket.emit('create_game');
});

btnJoin.addEventListener('click', () => {
    const roomCode = roomInput.value.trim();
    if (roomCode) {
        socket.emit('join_game', { room: roomCode });
    }
});

cells.forEach(cell => {
    cell.addEventListener('click', () => {
        if (!isMyTurn || cell.textContent !== '') return;
        const index = cell.getAttribute('data-index');
        socket.emit('make_move', { room: currentRoom, index: index });
    });
});

btnReplay.addEventListener('click', () => {
    socket.emit('restart_game', { room: currentRoom });
});

// Socket Events
socket.on('game_created', (data) => {
    enterGame(data.room, 'X');
    playerStatus.textContent = 'Waiting for opponent...';
});

socket.on('game_joined', (data) => {
    enterGame(data.room, 'O');
    playerStatus.textContent = "Opponent's turn (X)";
});

socket.on('player_joined', () => {
    if (mySymbol === 'X') {
        playerStatus.textContent = "Your turn (X)";
        isMyTurn = true;
    }
});

socket.on('move_made', (data) => {
    const cell = document.querySelector(`.cell[data-index="${data.index}"]`);
    cell.textContent = data.symbol;
    cell.classList.add(data.symbol.toLowerCase());

    // Check for win/draw
    if (data.game_over) {
        isMyTurn = false;
        showResult(data.result);
    } else {
        isMyTurn = data.next_turn === mySymbol;
        playerStatus.textContent = isMyTurn ? `Your turn (${mySymbol})` : `Opponent's turn (${data.next_turn})`;
    }
});

socket.on('game_restarted', () => {
    resetBoard();
    gameResult.classList.add('hidden');
    // X starts
    isMyTurn = (mySymbol === 'X');
    playerStatus.textContent = isMyTurn ? `Your turn (${mySymbol})` : `Opponent's turn (X)`;
});

socket.on('error', (msg) => {
    alert(msg);
});

// Helper Functions
function enterGame(room, symbol) {
    currentRoom = room;
    mySymbol = symbol;
    landingPage.classList.add('hidden');
    gameRoom.classList.remove('hidden');
    displayRoomCode.textContent = room;
}

function showResult(result) {
    gameResult.classList.remove('hidden');
    if (result === 'draw') {
        resultMessage.textContent = "It's a Draw!";
    } else if (result === mySymbol) {
        resultMessage.textContent = "You Won!";
    } else {
        resultMessage.textContent = "You Lost!";
    }
}

function resetBoard() {
    cells.forEach(cell => {
        cell.textContent = '';
        cell.className = 'cell';
    });
}
