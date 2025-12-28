/**
 * WebRTC Client Implementation
 * Handles peer connections, media streams, and signaling
 */

class WebRTCClient {
    constructor() {
        this.peerConnections = new Map(); // userId -> RTCPeerConnection
        this.localStream = null;
        this.dataChannels = new Map(); // userId -> RTCDataChannel
        
        // ICE servers configuration
        this.iceServers = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
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

        // Handle connection state changes
        pc.onconnectionstatechange = () => {
            console.log(`Connection state for ${userId}:`, pc.connectionState);
            this.onConnectionStateChange?.(userId, pc.connectionState);
            
            if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
                this.removePeerConnection(userId);
            }
        };

        // Handle incoming tracks
        pc.ontrack = (event) => {
            console.log(`Received remote track from ${userId}`);
            this.onRemoteStream?.(userId, event.streams[0]);
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
        }

        try {
            const offer = await pc.createOffer();
            await pc.setLocalDescription(offer);
            return offer;
        } catch (error) {
            console.error('Error creating offer:', error);
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
        }

        try {
            await pc.setRemoteDescription(new RTCSessionDescription(offer));
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
                await pc.addIceCandidate(new RTCIceCandidate(candidate));
            } catch (error) {
                console.error('Error adding ICE candidate:', error);
            }
        }
    }

    /**
     * Remove a peer connection
     */
    removePeerConnection(userId) {
        const pc = this.peerConnections.get(userId);
        if (pc) {
            pc.close();
            this.peerConnections.delete(userId);
        }

        const dc = this.dataChannels.get(userId);
        if (dc) {
            dc.close();
            this.dataChannels.delete(userId);
        }

        this.onRemoteStreamRemoved?.(userId);
    }

    /**
     * Close all connections and cleanup
     */
    cleanup() {
        // Close all peer connections
        this.peerConnections.forEach((pc, userId) => {
            pc.close();
        });
        this.peerConnections.clear();

        // Close all data channels
        this.dataChannels.forEach((dc, userId) => {
            dc.close();
        });
        this.dataChannels.clear();

        // Stop local stream
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
            this.localStream = null;
        }
    }
}

// Export for use in other modules
window.WebRTCClient = WebRTCClient;
