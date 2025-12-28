/**
 * Chat Module
 * Handles text messaging functionality
 */

class ChatManager {
    constructor() {
        this.messages = [];
        this.unreadCount = 0;
        this.isVisible = false;

        // DOM elements
        this.messagesContainer = null;
        this.chatForm = null;
        this.chatInput = null;
        this.unreadBadge = null;

        // Callbacks
        this.onSendMessage = null;
    }

    /**
     * Initialize chat with DOM elements
     */
    init() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.unreadBadge = document.getElementById('unread-badge');

        // Handle form submission
        this.chatForm?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
    }

    /**
     * Send a message
     */
    sendMessage() {
        const text = this.chatInput?.value.trim();
        if (!text) return;

        const message = {
            type: 'chat',
            text: text,
            timestamp: new Date().toISOString()
        };

        this.onSendMessage?.(message);
        this.chatInput.value = '';
    }

    /**
     * Add a message to the chat
     */
    addMessage(message, isSent = false) {
        this.messages.push(message);

        const messageEl = document.createElement('div');
        messageEl.className = `chat-message ${isSent ? 'sent' : 'received'}`;

        const time = new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageEl.innerHTML = `
            ${!isSent ? `<div class="sender">${this.escapeHtml(message.from_username || 'Unknown')}</div>` : ''}
            <div class="text">${this.escapeHtml(message.message || message.text)}</div>
            <div class="time">${time}</div>
        `;

        // Remove welcome message if exists
        const welcome = this.messagesContainer?.querySelector('.chat-welcome');
        if (welcome) {
            welcome.remove();
        }

        this.messagesContainer?.appendChild(messageEl);
        this.scrollToBottom();

        // Update unread count if chat is not visible
        if (!this.isVisible && !isSent) {
            this.unreadCount++;
            this.updateUnreadBadge();
        }
    }

    /**
     * Scroll chat to bottom
     */
    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }

    /**
     * Update unread badge
     */
    updateUnreadBadge() {
        if (this.unreadBadge) {
            if (this.unreadCount > 0) {
                this.unreadBadge.textContent = this.unreadCount > 99 ? '99+' : this.unreadCount;
                this.unreadBadge.classList.add('visible');
            } else {
                this.unreadBadge.classList.remove('visible');
            }
        }
    }

    /**
     * Set chat visibility
     */
    setVisible(visible) {
        this.isVisible = visible;
        if (visible) {
            this.unreadCount = 0;
            this.updateUnreadBadge();
            this.scrollToBottom();
        }
    }

    /**
     * Clear all messages
     */
    clear() {
        this.messages = [];
        this.unreadCount = 0;
        this.updateUnreadBadge();

        if (this.messagesContainer) {
            this.messagesContainer.innerHTML = `
                <div class="chat-welcome">
                    <p>Messages are shared with everyone in the call</p>
                </div>
            `;
        }
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Add system message
     */
    addSystemMessage(text) {
        const messageEl = document.createElement('div');
        messageEl.className = 'chat-message system';
        messageEl.style.cssText = 'align-self: center; background: transparent; color: var(--text-muted); font-size: 0.8rem; text-align: center;';
        messageEl.textContent = text;

        this.messagesContainer?.appendChild(messageEl);
        this.scrollToBottom();
    }
}

// Export for use in other modules
window.ChatManager = ChatManager;
