const socket = io();

// UI Elements
const landingPage = document.getElementById('landing-page');
const gameRoom = document.getElementById('game-room');
const btnCreate = document.getElementById('btn-create');
const btnJoin = document.getElementById('btn-join');
const roundsSelect = document.getElementById('rounds-select');
const roomInput = document.getElementById('room-code-input');
const displayRoom = document.getElementById('display-room-code');
const roundsInfo = document.getElementById('rounds-info');
const gameStatus = document.getElementById('game-status');
const actionsArea = document.getElementById('actions-area');
const scoreYou = document.getElementById('score-you-val');
const scoreOpp = document.getElementById('score-opp-val');
const moveBtns = document.querySelectorAll('.move-btn');
const resultModal = document.getElementById('result-modal');
const finalResultMsg = document.getElementById('final-result-msg');
const btnReplay = document.getElementById('btn-replay');

let currentRoom = null;
let hasMoved = false;

// Listeners
btnCreate.addEventListener('click', () => {
    const rounds = parseInt(roundsSelect.value);
    socket.emit('create_game', { rounds: rounds });
});

btnJoin.addEventListener('click', () => {
    const room = roomInput.value.trim().toUpperCase();
    if (room) {
        socket.emit('join_game', { room: room });
    }
});

moveBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        if (hasMoved) return;

        const move = btn.getAttribute('data-move');
        socket.emit('make_move', { room: currentRoom, move: move });

        // UI Feedback
        btn.classList.add('selected');
        gameStatus.textContent = `You picked ${move.toUpperCase()}`;
        hasMoved = true;
        disableMoves(true);
    });
});

btnReplay.addEventListener('click', () => {
    socket.emit('restart_game', { room: currentRoom });
});

// Socket Events
socket.on('game_created', (data) => {
    enterGame(data.room);
    updateRoundInfo(1, data.total_rounds);
    gameStatus.textContent = `Room created! Rule: Best of ${data.total_rounds}`;
});

socket.on('game_joined', (data) => {
    enterGame(data.room);
    updateRoundInfo(data.current_round, data.total_rounds); // Sync status
    gameStatus.textContent = "Waiting for game start...";
});

socket.on('start_round', (data) => {
    updateRoundInfo(data.round, data.total_rounds);
    resetRoundUI();
    gameStatus.textContent = "MAKE YOUR MOVE!";
    actionsArea.classList.remove('hidden');
});

socket.on('error', (msg) => {
    alert(msg);
});

socket.on('round_result', (data) => {
    // Display the round result clearly
    const resultText = data.result === 'draw' ? "IT'S A DRAW!" : (data.result === 'win' ? "YOU WON THIS ROUND!" : "YOU LOST THIS ROUND!");
    gameStatus.textContent = `${resultText} - Opponent picked ${data.opp_move.toUpperCase()}`;

    // Update scores immediately
    scoreYou.textContent = data.new_scores.you;
    scoreOpp.textContent = data.new_scores.opp;

    // Keep the actions visible but disabled briefly to show what was picked
    disableMoves(true);

    // After showing result, prepare for next round or game over
    setTimeout(() => {
        if (!data.game_over) {
            gameStatus.textContent = "Next round starting...";
        }
    }, 2500);
});

socket.on('game_over', (data) => {
    setTimeout(() => {
        resultModal.classList.remove('hidden');
        if (data.winner === 'draw') {
            finalResultMsg.textContent = "IT'S A DRAW!";
        } else if (data.winner === 'you') {
            finalResultMsg.textContent = "VICTORY!";
        } else {
            finalResultMsg.textContent = "DEFEAT!";
        }
        actionsArea.classList.add('hidden');
    }, 1500);
});

socket.on('game_restarted', (data) => {
    // Reset everything
    resultModal.classList.add('hidden');
    scoreYou.textContent = '0';
    scoreOpp.textContent = '0';
    updateRoundInfo(1, data.total_rounds);
    // Wait for start_round event or it might come immediately
});

// Helpers
function enterGame(room) {
    currentRoom = room;
    landingPage.classList.add('hidden');
    gameRoom.classList.remove('hidden');
    displayRoom.textContent = room;
}

function updateRoundInfo(current, total) {
    roundsInfo.textContent = `ROUND ${current}/${total}`;
}

function resetRoundUI() {
    hasMoved = false;
    moveBtns.forEach(btn => btn.classList.remove('selected'));
    disableMoves(false);
}

function disableMoves(disable) {
    moveBtns.forEach(btn => btn.disabled = disable);
}
