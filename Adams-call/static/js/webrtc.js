/**
 * WebRTC Client Implementation
 * Handles peer connections, media streams, and signaling
 */

class WebRTCClient {
    constructor() {
        this.peerConnections = new Map(); // userId -> RTCPeerConnection
        this.localStream = null;
        this.dataChannels = new Map(); // userId -> RTCDataChannel
        this.pendingCandidates = new Map(); // userId -> ICE candidates queue
        this.connectionInProgress = new Map(); // userId -> boolean (prevents duplicate connections)
        
        // ICE servers configuration
        this.iceServers = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' },
                { urls: 'stun:stun2.l.google.com:19302' },
                { urls: 'stun:stun3.l.google.com:19302' }
            ],
            iceCandidatePoolSize: 10
        };
        
        // Callbacks
        this.onRemoteStream = null;
        this.onRemoteStreamRemoved = null;
        this.onDataChannelMessage = null;
        this.onConnectionStateChange = null;
    }

    /**
     * Get local media stream (camera and microphone)
     */
    async getLocalStream(videoEnabled = true, audioEnabled = true) {
        try {
            const constraints = {
                video: videoEnabled ? {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user'
                } : false,
                audio: audioEnabled ? {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                } : false
            };

            this.localStream = await navigator.mediaDevices.getUserMedia(constraints);
            return this.localStream;
        } catch (error) {
            console.error('Error getting local stream:', error);
            throw error;
        }
    }

    /**
     * Toggle audio track
     */
    toggleAudio() {
        if (this.localStream) {
            const audioTracks = this.localStream.getAudioTracks();
            audioTracks.forEach(track => {
                track.enabled = !track.enabled;
            });
            return audioTracks[0]?.enabled ?? false;
        }
        return false;
    }

    /**
     * Toggle video track
     */
    toggleVideo() {
        if (this.localStream) {
            const videoTracks = this.localStream.getVideoTracks();
            videoTracks.forEach(track => {
                track.enabled = !track.enabled;
            });
            return videoTracks[0]?.enabled ?? false;
        }
        return false;
    }

    /**
     * Create a new peer connection for a user
     */
    createPeerConnection(userId, isInitiator = false) {
        // Check if we already have a connection or one is in progress
        if (this.peerConnections.has(userId)) {
            console.log(`Peer connection already exists for ${userId}`);
            return this.peerConnections.get(userId);
        }
        
        if (this.connectionInProgress.get(userId)) {
            console.log(`Connection already in progress for ${userId}`);
            return null;
        }
        
        this.connectionInProgress.set(userId, true);
        
        const pc = new RTCPeerConnection(this.iceServers);

        // Add local stream tracks
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => {
                pc.addTrack(track, this.localStream);
            });
        }

        // Handle ICE candidates
        pc.onicecandidate = (event) => {
            if (event.candidate) {
                this.onIceCandidate?.(userId, event.candidate);
            }
        };
        
        // Handle ICE connection state
        pc.oniceconnectionstatechange = () => {
            console.log(`ICE state for ${userId}:`, pc.iceConnectionState);
            if (pc.iceConnectionState === 'failed') {
                console.log(`ICE failed for ${userId}, restarting...`);
                pc.restartIce();
            }
        };

        // Handle connection state changes
        pc.onconnectionstatechange = () => {
            console.log(`Connection state for ${userId}:`, pc.connectionState);
            this.onConnectionStateChange?.(userId, pc.connectionState);
            
            if (pc.connectionState === 'connected') {
                this.connectionInProgress.delete(userId);
            } else if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
                this.connectionInProgress.delete(userId);
                // Delay removal to allow for reconnection attempts
                setTimeout(() => {
                    if (pc.connectionState === 'failed' || pc.connectionState === 'disconnected') {
                        this.removePeerConnection(userId);
                    }
                }, 5000);
            }
        };

        // Handle incoming tracks
        pc.ontrack = (event) => {
            console.log(`Received remote track from ${userId}`);
            if (event.streams && event.streams[0]) {
                this.onRemoteStream?.(userId, event.streams[0]);
            }
        };

        // Create data channel if initiator
        if (isInitiator) {
            const dataChannel = pc.createDataChannel('chat', {
                ordered: true
            });
            this.setupDataChannel(userId, dataChannel);
        }

        // Handle incoming data channels
        pc.ondatachannel = (event) => {
            this.setupDataChannel(userId, event.channel);
        };

        this.peerConnections.set(userId, pc);
        this.pendingCandidates.set(userId, []);
        return pc;
    }

    /**
     * Setup data channel for messaging
     */
    setupDataChannel(userId, channel) {
        channel.onopen = () => {
            console.log(`Data channel opened with ${userId}`);
        };

        channel.onclose = () => {
            console.log(`Data channel closed with ${userId}`);
        };

        channel.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                this.onDataChannelMessage?.(userId, data);
            } catch (e) {
                console.error('Error parsing data channel message:', e);
            }
        };

        this.dataChannels.set(userId, channel);
    }

    /**
     * Send message via data channel
     */
    sendDataChannelMessage(message) {
        const data = JSON.stringify(message);
        this.dataChannels.forEach((channel, userId) => {
            if (channel.readyState === 'open') {
                channel.send(data);
            }
        });
    }

    /**
     * Create and send an offer to a peer
     */
    async createOffer(userId) {
        let pc = this.peerConnections.get(userId);
        if (!pc) {
            pc = this.createPeerConnection(userId, true);
            if (!pc) {
                console.log(`Could not create peer connection for ${userId}`);
                return null;
            }
        }

        try {
            const offer = await pc.createOffer({
                offerToReceiveAudio: true,
                offerToReceiveVideo: true
            });
            await pc.setLocalDescription(offer);
            return offer;
        } catch (error) {
            console.error('Error creating offer:', error);
            this.connectionInProgress.delete(userId);
            throw error;
        }
    }

    /**
     * Handle an incoming offer and create an answer
     */
    async handleOffer(userId, offer) {
        let pc = this.peerConnections.get(userId);
        if (!pc) {
            pc = this.createPeerConnection(userId, false);
            if (!pc) {
                console.log(`Could not create peer connection for offer from ${userId}`);
                return null;
            }
        }

        try {
            // Handle glare (both sides sending offers)
            if (pc.signalingState !== 'stable') {
                console.log(`Handling glare for ${userId}, current state: ${pc.signalingState}`);
                await Promise.all([
                    pc.setLocalDescription({ type: 'rollback' }),
                    pc.setRemoteDescription(new RTCSessionDescription(offer))
                ]);
            } else {
                await pc.setRemoteDescription(new RTCSessionDescription(offer));
            }
            
            // Process any pending ICE candidates
            const pendingCandidates = this.pendingCandidates.get(userId) || [];
            for (const candidate of pendingCandidates) {
                await pc.addIceCandidate(new RTCIceCandidate(candidate));
            }
            this.pendingCandidates.set(userId, []);
            
            const answer = await pc.createAnswer();
            await pc.setLocalDescription(answer);
            return answer;
        } catch (error) {
            console.error('Error handling offer:', error);
            throw error;
        }
    }

    /**
     * Handle an incoming answer
     */
    async handleAnswer(userId, answer) {
        const pc = this.peerConnections.get(userId);
        if (pc) {
            try {
                await pc.setRemoteDescription(new RTCSessionDescription(answer));
            } catch (error) {
                console.error('Error handling answer:', error);
                throw error;
            }
        }
    }

    /**
     * Handle an incoming ICE candidate
     */
    async handleIceCandidate(userId, candidate) {
        const pc = this.peerConnections.get(userId);
        if (pc) {
            try {
                // Queue candidates if remote description not set yet
                if (!pc.remoteDescription || !pc.remoteDescription.type) {
                    console.log(`Queuing ICE candidate for ${userId}`);
                    const pending = this.pendingCandidates.get(userId) || [];
                    pending.push(candidate);
                    this.pendingCandidates.set(userId, pending);
                    return;
                }
                await pc.addIceCandidate(new RTCIceCandidate(candidate));
            } catch (error) {
                console.error('Error adding ICE candidate:', error);
            }
        } else {
            // Queue for later if peer connection doesn't exist yet
            console.log(`No peer connection for ${userId}, queuing candidate`);
            const pending = this.pendingCandidates.get(userId) || [];
            pending.push(candidate);
            this.pendingCandidates.set(userId, pending);
        }
    }

    /**
     * Remove a peer connection
     */
    removePeerConnection(userId) {
        console.log(`Removing peer connection for ${userId}`);
        
        const pc = this.peerConnections.get(userId);
        if (pc) {
            pc.onicecandidate = null;
            pc.ontrack = null;
            pc.ondatachannel = null;
            pc.onconnectionstatechange = null;
            pc.oniceconnectionstatechange = null;
            pc.close();
            this.peerConnections.delete(userId);
        }

        const dc = this.dataChannels.get(userId);
        if (dc) {
            dc.close();
            this.dataChannels.delete(userId);
        }
        
        this.pendingCandidates.delete(userId);
        this.connectionInProgress.delete(userId);

        this.onRemoteStreamRemoved?.(userId);
    }

    /**
     * Close all connections and cleanup
     */
    cleanup() {
        // Close all peer connections properly
        this.peerConnections.forEach((pc, userId) => {
            pc.onicecandidate = null;
            pc.ontrack = null;
            pc.ondatachannel = null;
            pc.onconnectionstatechange = null;
            pc.oniceconnectionstatechange = null;
            pc.close();
        });
        this.peerConnections.clear();

        // Close all data channels
        this.dataChannels.forEach((dc, userId) => {
            dc.close();
        });
        this.dataChannels.clear();
        
        // Clear pending candidates and connection states
        this.pendingCandidates.clear();
        this.connectionInProgress.clear();

        // Stop local stream
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
            this.localStream = null;
        }
    }
}

// Export for use in other modules
window.WebRTCClient = WebRTCClient;
