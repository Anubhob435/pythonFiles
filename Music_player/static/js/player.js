// Global variables
let playlist = [];
let currentSongIndex = -1;
let isPlaying = false;
let isShuffle = false;
let repeatMode = 0; // 0: no repeat, 1: repeat all, 2: repeat one

// DOM elements
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const shuffleBtn = document.getElementById('shuffleBtn');
const repeatBtn = document.getElementById('repeatBtn');
const progressBar = document.getElementById('progressBar');
const progressFill = document.getElementById('progressFill');
const currentTimeEl = document.getElementById('currentTime');
const durationEl = document.getElementById('duration');
const volumeSlider = document.getElementById('volumeSlider');
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const playlistEl = document.getElementById('playlist');
const currentSongTitle = document.getElementById('currentSongTitle');
const currentSongArtist = document.getElementById('currentSongArtist');
const playlistCount = document.getElementById('playlistCount');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPlaylist();
    setupEventListeners();
    updatePlaylistCount();
});

// Setup event listeners
function setupEventListeners() {
    // Player controls
    playPauseBtn.addEventListener('click', togglePlayPause);
    prevBtn.addEventListener('click', playPrevious);
    nextBtn.addEventListener('click', playNext);
    shuffleBtn.addEventListener('click', toggleShuffle);
    repeatBtn.addEventListener('click', toggleRepeat);

    // Audio events
    audioPlayer.addEventListener('timeupdate', updateProgress);
    audioPlayer.addEventListener('loadedmetadata', updateDuration);
    audioPlayer.addEventListener('ended', handleSongEnd);

    // Progress bar
    progressBar.addEventListener('click', seek);

    // Volume
    volumeSlider.addEventListener('input', changeVolume);
    audioPlayer.volume = volumeSlider.value / 100;

    // File upload
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());
}

// Load playlist from server
async function loadPlaylist() {
    try {
        const response = await fetch('/playlist');
        playlist = await response.json();
        renderPlaylist();
        updatePlaylistCount();
    } catch (error) {
        console.error('Error loading playlist:', error);
        showToast('Error loading playlist', 'error');
    }
}

// Render playlist
function renderPlaylist() {
    if (playlist.length === 0) {
        playlistEl.innerHTML = `
            <div class="empty-playlist">
                <i class="fas fa-music"></i>
                <p>No songs in playlist</p>
                <p class="hint">Upload some music to get started!</p>
            </div>
        `;
        return;
    }

    playlistEl.innerHTML = playlist.map((song, index) => `
        <div class="playlist-item ${index === currentSongIndex ? 'active' : ''}" 
             data-index="${index}" 
             data-id="${song.id}"
             onclick="playSong(${index})">
            <div class="song-number">${index + 1}</div>
            <div class="song-details">
                <div class="song-title">${song.title}</div>
            </div>
            <div class="song-actions">
                <button class="btn-play-song" onclick="event.stopPropagation(); playSong(${index})">
                    <i class="fas fa-play"></i>
                </button>
                <button class="btn-delete" onclick="event.stopPropagation(); deleteSong(${song.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Play song by index
function playSong(index) {
    if (index < 0 || index >= playlist.length) return;

    currentSongIndex = index;
    const song = playlist[index];

    audioPlayer.src = `/stream/${song.id}`;
    audioPlayer.play();
    isPlaying = true;
    updatePlayPauseButton();
    updateNowPlaying(song);
    renderPlaylist();
}

// Play song by ID
function playSongById(songId) {
    const index = playlist.findIndex(song => song.id === songId);
    if (index !== -1) {
        playSong(index);
    }
}

// Toggle play/pause
function togglePlayPause() {
    if (playlist.length === 0) {
        showToast('Playlist is empty', 'error');
        return;
    }

    if (audioPlayer.src === '') {
        playSong(0);
        return;
    }

    if (isPlaying) {
        audioPlayer.pause();
        isPlaying = false;
    } else {
        audioPlayer.play();
        isPlaying = true;
    }
    updatePlayPauseButton();
}

// Update play/pause button
function updatePlayPauseButton() {
    const icon = playPauseBtn.querySelector('i');
    if (isPlaying) {
        icon.className = 'fas fa-pause';
    } else {
        icon.className = 'fas fa-play';
    }
}

// Play previous song
function playPrevious() {
    if (currentSongIndex > 0) {
        playSong(currentSongIndex - 1);
    } else {
        playSong(playlist.length - 1);
    }
}

// Play next song
function playNext() {
    if (isShuffle) {
        const randomIndex = Math.floor(Math.random() * playlist.length);
        playSong(randomIndex);
    } else if (currentSongIndex < playlist.length - 1) {
        playSong(currentSongIndex + 1);
    } else {
        playSong(0);
    }
}

// Handle song end
function handleSongEnd() {
    if (repeatMode === 2) {
        // Repeat one
        audioPlayer.play();
    } else if (repeatMode === 1 || currentSongIndex < playlist.length - 1) {
        // Repeat all or not last song
        playNext();
    } else {
        // Last song and no repeat
        isPlaying = false;
        updatePlayPauseButton();
    }
}

// Toggle shuffle
function toggleShuffle() {
    isShuffle = !isShuffle;
    shuffleBtn.classList.toggle('active', isShuffle);
    showToast(isShuffle ? 'Shuffle ON' : 'Shuffle OFF', 'success');
}

// Toggle repeat
function toggleRepeat() {
    repeatMode = (repeatMode + 1) % 3;
    const icon = repeatBtn.querySelector('i');
    
    if (repeatMode === 0) {
        repeatBtn.classList.remove('active');
        icon.className = 'fas fa-redo';
        showToast('Repeat OFF', 'success');
    } else if (repeatMode === 1) {
        repeatBtn.classList.add('active');
        icon.className = 'fas fa-redo';
        showToast('Repeat All', 'success');
    } else {
        repeatBtn.classList.add('active');
        icon.className = 'fas fa-redo-alt';
        showToast('Repeat One', 'success');
    }
}

// Update progress bar
function updateProgress() {
    const { currentTime, duration } = audioPlayer;
    if (duration) {
        const progressPercent = (currentTime / duration) * 100;
        progressFill.style.width = `${progressPercent}%`;
        currentTimeEl.textContent = formatTime(currentTime);
    }
}

// Update duration
function updateDuration() {
    durationEl.textContent = formatTime(audioPlayer.duration);
}

// Seek in song
function seek(e) {
    const width = progressBar.clientWidth;
    const clickX = e.offsetX;
    const duration = audioPlayer.duration;
    audioPlayer.currentTime = (clickX / width) * duration;
}

// Change volume
function changeVolume(e) {
    audioPlayer.volume = e.target.value / 100;
}

// Update now playing
function updateNowPlaying(song) {
    currentSongTitle.textContent = song.title;
    currentSongArtist.textContent = 'Now Playing';
}

// Format time
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Update playlist count
function updatePlaylistCount() {
    playlistCount.textContent = `${playlist.length} song${playlist.length !== 1 ? 's' : ''}`;
}

// File upload handling
async function handleFileSelect(e) {
    const files = e.target.files;
    await uploadFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

async function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    await uploadFiles(files);
}

// Upload files
async function uploadFiles(files) {
    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            showToast(`Uploading ${file.name}...`, 'success');
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                playlist.push(result.song);
                showToast(`${file.name} uploaded successfully!`, 'success');
            } else {
                showToast(`Failed to upload ${file.name}`, 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            showToast(`Error uploading ${file.name}`, 'error');
        }
    }

    renderPlaylist();
    updatePlaylistCount();
    fileInput.value = ''; // Reset input
}

// Delete song
async function deleteSong(songId) {
    if (!confirm('Are you sure you want to delete this song?')) return;

    try {
        const response = await fetch(`/delete/${songId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            // Remove from playlist array
            const index = playlist.findIndex(song => song.id === songId);
            if (index !== -1) {
                playlist.splice(index, 1);
            }

            // If deleted song was playing, stop playback
            if (index === currentSongIndex) {
                audioPlayer.pause();
                audioPlayer.src = '';
                isPlaying = false;
                currentSongIndex = -1;
                updatePlayPauseButton();
                currentSongTitle.textContent = 'No song playing';
                currentSongArtist.textContent = 'Select a song from the playlist';
            } else if (index < currentSongIndex) {
                currentSongIndex--;
            }

            renderPlaylist();
            updatePlaylistCount();
            showToast('Song deleted successfully', 'success');
        }
    } catch (error) {
        console.error('Delete error:', error);
        showToast('Error deleting song', 'error');
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
        togglePlayPause();
    } else if (e.code === 'ArrowLeft') {
        audioPlayer.currentTime -= 5;
    } else if (e.code === 'ArrowRight') {
        audioPlayer.currentTime += 5;
    } else if (e.code === 'ArrowUp') {
        e.preventDefault();
        volumeSlider.value = Math.min(100, parseInt(volumeSlider.value) + 10);
        changeVolume({ target: volumeSlider });
    } else if (e.code === 'ArrowDown') {
        e.preventDefault();
        volumeSlider.value = Math.max(0, parseInt(volumeSlider.value) - 10);
        changeVolume({ target: volumeSlider });
    }
});
