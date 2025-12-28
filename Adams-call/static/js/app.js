/**
 * Main Application Logic
 * Handles UI interactions, authentication, and coordinates WebRTC/Chat
 */

class App {
    constructor() {
        // State
        this.currentUser = null;
        this.currentRoom = null;
        this.token = null;
        this.ws = null;
        this.participants = new Map(); // userId -> participant info

        // Components
        this.webrtc = new WebRTCClient();
        this.chat = new ChatManager();

        // DOM Screens
        this.authScreen = document.getElementById('auth-screen');
        this.lobbyScreen = document.getElementById('lobby-screen');
        this.callScreen = document.getElementById('call-screen');

        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.setupAuthHandlers();
        this.setupLobbyHandlers();
        this.setupCallHandlers();
        this.setupWebRTCCallbacks();
        this.chat.init();

        // Check for saved session
        const savedToken = localStorage.getItem('auth_token');
        const savedUser = localStorage.getItem('user_data');
        if (savedToken && savedUser) {
            this.token = savedToken;
            this.currentUser = JSON.parse(savedUser);
            this.showScreen('lobby');
            this.updateUserDisplay();
        }
    }

    /**
     * Setup authentication form handlers
     */
    setupAuthHandlers() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
                btn.classList.add('active');
                const form = document.getElementById(`${btn.dataset.tab}-form`);
                form?.classList.add('active');
                this.clearAuthError();
            });
        });

        // Login form
        document.getElementById('login-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form
        document.getElementById('register-form')?.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Logout button
        document.getElementById('logout-btn')?.addEventListener('click', () => {
            this.handleLogout();
        });
    }

    /**
     * Setup lobby handlers
     */
    setupLobbyHandlers() {
        // Create room
        document.getElementById('create-room-btn')?.addEventListener('click', async () => {
            await this.createRoom();
        });

        // Join room
        document.getElementById('join-room-btn')?.addEventListener('click', async () => {
            const code = document.getElementById('room-code-input')?.value.trim();
            if (code) {
                await this.joinRoom(code);
            }
        });

        // Enter key for room code
        document.getElementById('room-code-input')?.addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                const code = e.target.value.trim();
                if (code) {
                    await this.joinRoom(code);
                }
            }
        });
    }

    /**
     * Setup call screen handlers
     */
    setupCallHandlers() {
        // Toggle audio
        document.getElementById('toggle-audio-btn')?.addEventListener('click', () => {
            const enabled = this.webrtc.toggleAudio();
            const btn = document.getElementById('toggle-audio-btn');
            btn?.classList.toggle('active', enabled);
            this.updateLocalMicStatus(enabled);
            this.sendMediaState({ audio_enabled: enabled });
        });

        // Toggle video
        document.getElementById('toggle-video-btn')?.addEventListener('click', () => {
            const enabled = this.webrtc.toggleVideo();
            const btn = document.getElementById('toggle-video-btn');
            btn?.classList.toggle('active', enabled);
            this.sendMediaState({ video_enabled: enabled });
        });

        // Toggle chat
        document.getElementById('toggle-chat-btn')?.addEventListener('click', () => {
            const panel = document.getElementById('chat-panel');
            const btn = document.getElementById('toggle-chat-btn');
            const isActive = panel?.classList.toggle('active');
            btn?.classList.toggle('active', isActive);
            this.chat.setVisible(isActive);
        });

        // Close chat
        document.getElementById('close-chat-btn')?.addEventListener('click', () => {
            document.getElementById('chat-panel')?.classList.remove('active');
            document.getElementById('toggle-chat-btn')?.classList.remove('active');
            this.chat.setVisible(false);
        });

        // End call
        document.getElementById('end-call-btn')?.addEventListener('click', () => {
            this.leaveRoom();
        });

        // Copy room code
        document.getElementById('copy-code-btn')?.addEventListener('click', () => {
            const code = document.getElementById('room-code-display')?.textContent;
            if (code) {
                navigator.clipboard.writeText(code);
                this.showToast('Room code copied!', 'success');
            }
        });

        // Chat send
        this.chat.onSendMessage = (message) => {
            this.sendChatMessage(message);
        };
    }

    /**
     * Setup WebRTC callbacks
     */
    setupWebRTCCallbacks() {
        // Handle ICE candidates
        this.webrtc.onIceCandidate = (userId, candidate) => {
            this.sendSignalingMessage({
                type: 'ice_candidate',
                target_user_id: userId,
                candidate: candidate
            });
        };

        // Handle remote stream
        this.webrtc.onRemoteStream = (userId, stream) => {
            this.addRemoteVideo(userId, stream);
        };

        // Handle remote stream removed
        this.webrtc.onRemoteStreamRemoved = (userId) => {
            this.removeRemoteVideo(userId);
        };

        // Handle connection state changes
        this.webrtc.onConnectionStateChange = (userId, state) => {
            console.log(`Connection to ${userId}: ${state}`);
        };

        // Handle data channel messages
        this.webrtc.onDataChannelMessage = (userId, data) => {
            if (data.type === 'chat') {
                this.chat.addMessage({
                    from_username: this.participants.get(userId)?.username || 'Unknown',
                    message: data.text,
                    timestamp: data.timestamp
                }, false);
            }
        };
    }

    /**
     * Handle login
     */
    async handleLogin() {
        const username = document.getElementById('login-username')?.value.trim();
        const password = document.getElementById('login-password')?.value;

        if (!username || !password) {
            this.showAuthError('Please fill in all fields');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.token = data.token;
                this.currentUser = {
                    user_id: data.user_id,
                    username: data.username
                };
                localStorage.setItem('auth_token', this.token);
                localStorage.setItem('user_data', JSON.stringify(this.currentUser));
                this.updateUserDisplay();
                this.showScreen('lobby');
                this.showToast(`Welcome back, ${data.username}!`, 'success');
            } else {
                this.showAuthError(data.error || 'Login failed');
            }
        } catch (error) {
            this.showAuthError('Connection error. Please try again.');
            console.error('Login error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Handle registration
     */
    async handleRegister() {
        const username = document.getElementById('register-username')?.value.trim();
        const password = document.getElementById('register-password')?.value;
        const confirm = document.getElementById('register-confirm')?.value;

        if (!username || !password || !confirm) {
            this.showAuthError('Please fill in all fields');
            return;
        }

        if (password !== confirm) {
            this.showAuthError('Passwords do not match');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.token = data.token;
                this.currentUser = {
                    user_id: data.user_id,
                    username: data.username
                };
                localStorage.setItem('auth_token', this.token);
                localStorage.setItem('user_data', JSON.stringify(this.currentUser));
                this.updateUserDisplay();
                this.showScreen('lobby');
                this.showToast(`Welcome, ${data.username}!`, 'success');
            } else {
                this.showAuthError(data.error || 'Registration failed');
            }
        } catch (error) {
            this.showAuthError('Connection error. Please try again.');
            console.error('Registration error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Handle logout
     */
    handleLogout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_data');
        this.showScreen('auth');
    }

    /**
     * Connect WebSocket
     */
    connectWebSocket() {
        return new Promise((resolve, reject) => {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            this.ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

            this.ws.onopen = () => {
                console.log('WebSocket connected');
                // Authenticate
                this.sendSignalingMessage({
                    type: 'auth',
                    token: this.token
                });
            };

            this.ws.onmessage = async (event) => {
                const data = JSON.parse(event.data);
                await this.handleSignalingMessage(data);

                if (data.type === 'auth_success') {
                    resolve();
                } else if (data.type === 'auth_error') {
                    reject(new Error(data.error));
                }
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                if (this.currentRoom) {
                    this.showToast('Connection lost. Returning to lobby...', 'error');
                    this.cleanupCall();
                    this.showScreen('lobby');
                }
            };
        });
    }

    /**
     * Send signaling message
     */
    sendSignalingMessage(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    /**
     * Handle signaling messages
     */
    async handleSignalingMessage(data) {
        console.log('Received:', data.type);

        switch (data.type) {
            case 'room_created':
            case 'room_joined':
                this.currentRoom = {
                    room_id: data.room_id,
                    room_code: data.room_code
                };
                document.getElementById('room-code-display').textContent = data.room_code;

                // Start local video
                await this.startLocalVideo();
                this.showScreen('call');

                // If there are existing participants, initiate connections sequentially
                if (data.participants && data.participants.length > 0) {
                    for (const p of data.participants) {
                        this.participants.set(p.user_id, p);
                    }
                    this.updateParticipantsCount();
                    
                    // Connect to each participant with a delay to prevent overwhelming
                    this.connectToParticipants(data.participants);
                }
                break;

            case 'user_joined':
                this.participants.set(data.user_id, {
                    user_id: data.user_id,
                    username: data.username
                });
                this.updateParticipantsCount();
                this.chat.addSystemMessage(`${data.username} joined the call`);
                this.showToast(`${data.username} joined`, 'info');
                break;

            case 'user_left':
                this.participants.delete(data.user_id);
                this.webrtc.removePeerConnection(data.user_id);
                this.removeRemoteVideo(data.user_id);
                this.updateParticipantsCount();
                this.chat.addSystemMessage(`${data.username} left the call`);
                this.showToast(`${data.username} left`, 'info');
                break;

            case 'offer':
                try {
                    const answer = await this.webrtc.handleOffer(data.from_user_id, data.offer);
                    if (answer) {
                        this.sendSignalingMessage({
                            type: 'answer',
                            target_user_id: data.from_user_id,
                            answer: answer
                        });
                    }
                } catch (error) {
                    console.error('Error handling offer:', error);
                }
                break;

            case 'answer':
                try {
                    await this.webrtc.handleAnswer(data.from_user_id, data.answer);
                } catch (error) {
                    console.error('Error handling answer:', error);
                }
                break;

            case 'ice_candidate':
                try {
                    await this.webrtc.handleIceCandidate(data.from_user_id, data.candidate);
                } catch (error) {
                    console.error('Error handling ICE candidate:', error);
                }
                break;

            case 'chat_message':
                if (data.from_user_id !== this.currentUser.user_id) {
                    this.chat.addMessage(data, false);
                }
                break;

            case 'media_state':
                this.updateRemoteMediaState(data);
                break;

            case 'error':
                this.showToast(data.error, 'error');
                break;
        }
    }

    /**
     * Create a new room
     */
    async createRoom() {
        this.showLoading(true);
        try {
            await this.connectWebSocket();
            this.sendSignalingMessage({ type: 'create_room' });
        } catch (error) {
            this.showToast('Failed to create room', 'error');
            console.error('Create room error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Join an existing room
     */
    async joinRoom(code) {
        this.showLoading(true);
        try {
            await this.connectWebSocket();
            this.sendSignalingMessage({
                type: 'join_room',
                room_code: code.toUpperCase()
            });
        } catch (error) {
            this.showToast('Failed to join room', 'error');
            console.error('Join room error:', error);
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Leave current room
     */
    leaveRoom() {
        this.sendSignalingMessage({ type: 'leave_room' });
        this.cleanupCall();
        this.showScreen('lobby');
    }

    /**
     * Cleanup after call ends
     */
    cleanupCall() {
        this.webrtc.cleanup();
        this.participants.clear();
        this.currentRoom = null;
        this.chat.clear();

        // Close WebSocket
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }

        // Remove remote videos
        const grid = document.getElementById('video-grid');
        const remoteVideos = grid?.querySelectorAll('.remote-video-wrapper');
        remoteVideos?.forEach(el => el.remove());

        // Clear local video
        const localVideo = document.getElementById('local-video');
        if (localVideo) {
            localVideo.srcObject = null;
        }

        // Reset UI
        document.getElementById('chat-panel')?.classList.remove('active');
        document.getElementById('toggle-chat-btn')?.classList.remove('active');
        document.getElementById('toggle-audio-btn')?.classList.add('active');
        document.getElementById('toggle-video-btn')?.classList.add('active');
    }

    /**
     * Start local video
     */
    async startLocalVideo() {
        try {
            const stream = await this.webrtc.getLocalStream(true, true);
            const localVideo = document.getElementById('local-video');
            if (localVideo) {
                localVideo.srcObject = stream;
            }
        } catch (error) {
            console.error('Error starting local video:', error);
            this.showToast('Could not access camera/microphone', 'error');
        }
    }

    /**
     * Connect to multiple participants sequentially with delays
     */
    async connectToParticipants(participants) {
        for (let i = 0; i < participants.length; i++) {
            const p = participants[i];
            // Small delay between connections to prevent overwhelming
            if (i > 0) {
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            
            try {
                const offer = await this.webrtc.createOffer(p.user_id);
                if (offer) {
                    this.sendSignalingMessage({
                        type: 'offer',
                        target_user_id: p.user_id,
                        offer: offer
                    });
                }
            } catch (error) {
                console.error(`Error connecting to ${p.username}:`, error);
            }
        }
    }

    /**
     * Add remote video element
     */
    addRemoteVideo(userId, stream) {
        const existingWrapper = document.getElementById(`video-${userId}`);
        if (existingWrapper) {
            const video = existingWrapper.querySelector('video');
            if (video) video.srcObject = stream;
            return;
        }

        const grid = document.getElementById('video-grid');
        const participant = this.participants.get(userId);

        const wrapper = document.createElement('div');
        wrapper.className = 'video-wrapper remote-video-wrapper';
        wrapper.id = `video-${userId}`;

        wrapper.innerHTML = `
            <video autoplay playsinline></video>
            <div class="video-label">
                <span class="video-name">${this.escapeHtml(participant?.username || 'User')}</span>
                <div class="video-status">
                    <span class="status-icon mic-on" id="mic-${userId}">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/>
                            <path d="M19 10v2a7 7 0 01-14 0v-2"/>
                        </svg>
                    </span>
                </div>
            </div>
        `;

        const video = wrapper.querySelector('video');
        video.srcObject = stream;

        // Insert before local video wrapper
        const localWrapper = document.querySelector('.local-video-wrapper');
        if (localWrapper) {
            grid?.insertBefore(wrapper, localWrapper);
        } else {
            grid?.appendChild(wrapper);
        }

        this.updateVideoLayout();
    }

    /**
     * Remove remote video element
     */
    removeRemoteVideo(userId) {
        const wrapper = document.getElementById(`video-${userId}`);
        if (wrapper) {
            wrapper.remove();
            this.updateVideoLayout();
        }
    }

    /**
     * Update video layout based on participant count
     */
    updateVideoLayout() {
        const grid = document.getElementById('video-grid');
        const remoteVideos = grid?.querySelectorAll('.remote-video-wrapper');
        const localWrapper = document.querySelector('.local-video-wrapper');

        if (remoteVideos?.length === 0) {
            // Only local video, make it full size
            localWrapper?.classList.add('full-size');
        } else {
            // Multiple participants
            localWrapper?.classList.remove('full-size');
        }
    }

    /**
     * Update participants count display
     */
    updateParticipantsCount() {
        const count = this.participants.size + 1; // Include self
        document.getElementById('participants-count').textContent = count;
    }

    /**
     * Update local mic status indicator
     */
    updateLocalMicStatus(enabled) {
        const status = document.getElementById('local-mic-status');
        if (status) {
            status.className = `status-icon ${enabled ? 'mic-on' : 'mic-off'}`;
        }
    }

    /**
     * Update remote media state
     */
    updateRemoteMediaState(data) {
        const micStatus = document.getElementById(`mic-${data.user_id}`);
        if (micStatus && data.audio_enabled !== undefined) {
            micStatus.className = `status-icon ${data.audio_enabled ? 'mic-on' : 'mic-off'}`;
        }
    }

    /**
     * Send media state update
     */
    sendMediaState(state) {
        this.sendSignalingMessage({
            type: 'media_state',
            ...state
        });
    }

    /**
     * Send chat message
     */
    sendChatMessage(message) {
        // Add to local chat
        this.chat.addMessage({
            from_username: this.currentUser.username,
            message: message.text,
            timestamp: message.timestamp
        }, true);

        // Send via WebSocket
        this.sendSignalingMessage({
            type: 'chat_message',
            message: message.text,
            timestamp: message.timestamp
        });

        // Also send via data channel for P2P
        this.webrtc.sendDataChannelMessage(message);
    }

    /**
     * Show a specific screen
     */
    showScreen(screen) {
        this.authScreen?.classList.remove('active');
        this.lobbyScreen?.classList.remove('active');
        this.callScreen?.classList.remove('active');

        switch (screen) {
            case 'auth':
                this.authScreen?.classList.add('active');
                break;
            case 'lobby':
                this.lobbyScreen?.classList.add('active');
                break;
            case 'call':
                this.callScreen?.classList.add('active');
                break;
        }
    }

    /**
     * Update user display in header
     */
    updateUserDisplay() {
        const usernameDisplay = document.getElementById('username-display');
        const avatarDisplay = document.getElementById('user-avatar');

        if (this.currentUser) {
            usernameDisplay.textContent = this.currentUser.username;
            avatarDisplay.textContent = this.currentUser.username.charAt(0).toUpperCase();
        }
    }

    /**
     * Show/hide loading overlay
     */
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        overlay?.classList.toggle('active', show);
    }

    /**
     * Show auth error message
     */
    showAuthError(message) {
        const errorEl = document.getElementById('auth-error');
        if (errorEl) {
            errorEl.textContent = message;
        }
    }

    /**
     * Clear auth error
     */
    clearAuthError() {
        const errorEl = document.getElementById('auth-error');
        if (errorEl) {
            errorEl.textContent = '';
        }
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${this.escapeHtml(message)}</span>
        `;

        container?.appendChild(toast);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /**
     * Escape HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});
