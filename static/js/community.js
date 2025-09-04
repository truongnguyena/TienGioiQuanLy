// Community Chat and Trading JavaScript functionality
class CommunityManager {
    constructor() {
        this.currentChannel = 'general';
        this.messagePollingTimer = null;
        this.init();
    }

    init() {
        this.setupChatSystem();
        this.setupModalHandlers();
        this.startMessagePolling();
        this.loadInitialMessages();
    }

    setupChatSystem() {
        // Chat form submission
        const chatForm = document.getElementById('chatForm');
        if (chatForm) {
            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }

        // Channel switching
        const channelSelect = document.getElementById('chatChannel');
        if (channelSelect) {
            channelSelect.addEventListener('change', (e) => {
                this.switchChannel(e.target.value);
            });
        }
    }

    setupModalHandlers() {
        // Setup modal close handlers for community modals
        document.addEventListener('click', (e) => {
            if (e.target.matches('.modal') && e.target.style.display === 'block') {
                this.closeModal(e.target.id);
            }
        });
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const content = messageInput.value.trim();
        
        if (!content) return;

        try {
            const response = await fetch('/api/send-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: content,
                    channel: this.currentChannel,
                    channel_id: this.currentChannel === 'guild' ? window.userGuildId : null
                })
            });

            const data = await response.json();

            if (data.success) {
                messageInput.value = '';
                this.loadMessages(); // Reload messages to show the new one
            } else {
                alert('Lỗi: ' + (data.error || 'Không thể gửi tin nhắn'));
            }
        } catch (error) {
            console.error('Error sending message:', error);
            alert('Có lỗi xảy ra khi gửi tin nhắn!');
        }
    }

    switchChannel(channel) {
        this.currentChannel = channel;
        this.loadMessages();
    }

    async loadMessages() {
        try {
            const response = await fetch(`/api/get-messages?channel=${this.currentChannel}`);
            const data = await response.json();

            if (data.success) {
                this.displayMessages(data.messages);
            }
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }

    loadInitialMessages() {
        // Load initial messages from server-rendered data if available
        const messagesContainer = document.getElementById('chatMessages');
        if (messagesContainer && messagesContainer.children.length === 1) {
            // Only loading spinner present, load messages
            this.loadMessages();
        }
    }

    displayMessages(messages) {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = '';

        if (messages.length === 0) {
            messagesContainer.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-comments text-muted" style="font-size: 3rem;"></i>
                    <p class="text-muted mt-2">Chưa có tin nhắn nào trong kênh này</p>
                </div>
            `;
            return;
        }

        messages.reverse().forEach(message => {
            const messageElement = this.createMessageElement(message);
            messagesContainer.appendChild(messageElement);
        });

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    createMessageElement(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${message.user_id === window.currentUserId ? 'own-message' : ''}`;
        
        const timeStr = new Date(message.created_at).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-author text-golden">${message.user_name}</span>
                <span class="message-time text-muted">${timeStr}</span>
            </div>
            <div class="message-content text-light">${this.escapeHtml(message.content)}</div>
        `;

        return messageDiv;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    startMessagePolling() {
        // Poll for new messages every 10 seconds
        this.messagePollingTimer = setInterval(() => {
            this.loadMessages();
        }, 10000);
    }

    stopMessagePolling() {
        if (this.messagePollingTimer) {
            clearInterval(this.messagePollingTimer);
            this.messagePollingTimer = null;
        }
    }

    // Modal management functions
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
            modal.style.backgroundColor = 'rgba(15, 15, 35, 0.8)';
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.style.overflow = '';
            
            // Remove any lingering backdrops
            const backdrops = document.querySelectorAll('.modal-backdrop');
            backdrops.forEach(backdrop => backdrop.remove());
            document.body.classList.remove('modal-open');
            document.body.style.paddingRight = '';
        }
    }
}

// Global functions for community features
function openBroadcastModal() {
    if (window.communityManager) {
        window.communityManager.openModal('broadcastModal');
    }
    // For now, show a simple prompt
    const message = prompt('Nhập thông báo thiên hạ (tốn 1000 linh thạch):');
    if (message && message.trim()) {
        fetch('/api/send-broadcast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message.trim() })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Đã gửi thông báo thiên hạ thành công!');
            } else {
                alert('Lỗi: ' + (data.error || 'Không thể gửi thông báo'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra!');
        });
    }
}

function openMentorRequestModal() {
    const request = prompt('Mô tả yêu cầu tìm sư phụ:');
    if (request && request.trim()) {
        fetch('/api/mentor-request', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ request: request.trim() })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Đã đăng yêu cầu tìm sư phụ thành công!');
            } else {
                alert('Lỗi: ' + (data.error || 'Không thể đăng yêu cầu'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra!');
        });
    }
}

function openTradeModal() {
    const itemName = prompt('Tên vật phẩm muốn giao dịch:');
    if (!itemName || !itemName.trim()) return;

    const quantity = prompt('Số lượng:');
    if (!quantity || isNaN(quantity) || parseInt(quantity) <= 0) {
        alert('Số lượng không hợp lệ!');
        return;
    }

    const price = prompt('Giá (linh thạch):');
    if (!price || isNaN(price) || parseInt(price) <= 0) {
        alert('Giá không hợp lệ!');
        return;
    }

    const type = prompt('Loại giao dịch:\n1. sell (Bán)\n2. buy (Mua)\n\nNhập loại:');
    if (!type || !['sell', 'buy'].includes(type.toLowerCase())) {
        alert('Loại giao dịch không hợp lệ!');
        return;
    }

    fetch('/api/create-trade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item_name: itemName.trim(),
            quantity: parseInt(quantity),
            price: parseInt(price),
            trade_type: type.toLowerCase()
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Đã đăng giao dịch thành công!');
        } else {
            alert('Lỗi: ' + (data.error || 'Không thể tạo giao dịch'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Có lỗi xảy ra khi tạo giao dịch!');
    });
}

function sendMessage(event) {
    if (event) {
        event.preventDefault();
    }
    if (window.communityManager) {
        window.communityManager.sendMessage();
    }
}

function switchChannel() {
    const channelSelect = document.getElementById('chatChannel');
    if (channelSelect && window.communityManager) {
        window.communityManager.switchChannel(channelSelect.value);
    }
}

// Initialize community manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.communityManager = new CommunityManager();
});