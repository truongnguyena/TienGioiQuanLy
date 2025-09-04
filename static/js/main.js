// Main JavaScript functionality for Tu Tien Community Platform
// Global variables and utilities

class TuTienApp {
    constructor() {
        this.currentUser = null;
        this.notifications = [];
        this.chatSocket = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeNotifications();
        this.startPeriodicUpdates();
        this.setupMysticalEffects();
    }

    setupEventListeners() {
        // Global click handlers
        document.addEventListener('click', (e) => {
            // Handle mystical button effects
            if (e.target.classList.contains('mystical-btn')) {
                this.createMysticalEffect(e.target);
            }

            // Handle card hover effects
            if (e.target.closest('.mystical-card')) {
                this.enhanceCardEffect(e.target.closest('.mystical-card'));
            }
        });

        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Quick cultivation (Ctrl + Space)
            if (e.ctrlKey && e.code === 'Space') {
                e.preventDefault();
                this.quickCultivate();
            }

            // Quick chat (Ctrl + Enter)
            if (e.ctrlKey && e.key === 'Enter') {
                const chatInput = document.getElementById('messageInput');
                if (chatInput && chatInput.value.trim()) {
                    e.preventDefault();
                    this.sendQuickMessage();
                }
            }
        });

        // Window resize handler
        window.addEventListener('resize', () => {
            this.handleResponsiveAdjustments();
        });

        // Page visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });
    }

    initializeNotifications() {
        // Check for browser notification permission
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }

        // Setup notification container
        this.createNotificationContainer();
    }

    createNotificationContainer() {
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'notification-container';
            container.innerHTML = `
                <style>
                .notification-container {
                    position: fixed;
                    top: 100px;
                    right: 20px;
                    z-index: 9999;
                    max-width: 400px;
                }
                .mystical-notification {
                    background: rgba(26, 26, 46, 0.95);
                    border: 1px solid rgba(255, 215, 0, 0.3);
                    border-radius: 10px;
                    padding: 1rem;
                    margin-bottom: 0.5rem;
                    backdrop-filter: blur(10px);
                    animation: slideInRight 0.3s ease-out;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                .notification-close {
                    float: right;
                    background: none;
                    border: none;
                    color: #ffd700;
                    cursor: pointer;
                    font-size: 1.2rem;
                }
                </style>
            `;
            document.body.appendChild(container);
        }
    }

    showNotification(title, message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `mystical-notification notification-${type}`;
        
        const iconMap = {
            'info': 'fas fa-info-circle',
            'success': 'fas fa-check-circle',
            'warning': 'fas fa-exclamation-triangle',
            'error': 'fas fa-times-circle',
            'cultivation': 'fas fa-meditation',
            'achievement': 'fas fa-trophy'
        };

        notification.innerHTML = `
            <button class="notification-close" onclick="this.parentElement.remove()">&times;</button>
            <div class="d-flex align-items-start">
                <i class="${iconMap[type] || iconMap.info} text-${this.getNotificationColor(type)} me-2 mt-1"></i>
                <div>
                    <h6 class="text-golden mb-1">${title}</h6>
                    <p class="text-light mb-0">${message}</p>
                </div>
            </div>
        `;

        container.appendChild(notification);

        // Auto remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);

        // Browser notification for important messages
        if (type === 'achievement' || type === 'warning') {
            this.showBrowserNotification(title, message);
        }
    }

    getNotificationColor(type) {
        const colorMap = {
            'info': 'celestial',
            'success': 'success',
            'warning': 'warning',
            'error': 'danger',
            'cultivation': 'purple',
            'achievement': 'golden'
        };
        return colorMap[type] || 'celestial';
    }

    showBrowserNotification(title, message) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`Tu Tiên - ${title}`, {
                body: message,
                icon: '/static/images/logo.png',
                badge: '/static/images/badge.png'
            });
        }
    }

    createMysticalEffect(element) {
        // Create floating particles effect
        for (let i = 0; i < 5; i++) {
            const particle = document.createElement('div');
            particle.className = 'mystical-particle';
            particle.style.cssText = `
                position: fixed;
                width: 4px;
                height: 4px;
                background: #ffd700;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9998;
                animation: floatUp 1s ease-out forwards;
            `;

            const rect = element.getBoundingClientRect();
            particle.style.left = (rect.left + Math.random() * rect.width) + 'px';
            particle.style.top = (rect.top + Math.random() * rect.height) + 'px';

            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 1000);
        }

        // Add CSS for particle animation if not exists
        if (!document.getElementById('mystical-effects-style')) {
            const style = document.createElement('style');
            style.id = 'mystical-effects-style';
            style.textContent = `
                @keyframes floatUp {
                    0% { transform: translateY(0) scale(1); opacity: 1; }
                    100% { transform: translateY(-50px) scale(0); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    enhanceCardEffect(card) {
        // Add subtle glow effect
        card.style.transition = 'all 0.3s ease';
        card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(255, 215, 0, 0.1)';
        
        setTimeout(() => {
            card.style.boxShadow = '';
        }, 300);
    }

    setupMysticalEffects() {
        // Floating particles background
        this.createFloatingParticles();

        // Mystical cursor trail
        this.setupCursorTrail();

        // Dynamic background effects
        this.setupDynamicBackground();
    }

    createFloatingParticles() {
        const particleContainer = document.querySelector('.floating-particles');
        if (!particleContainer) return;

        setInterval(() => {
            if (Math.random() < 0.3) { // 30% chance every interval
                const particle = document.createElement('div');
                particle.className = 'bg-particle';
                particle.style.cssText = `
                    position: absolute;
                    width: ${Math.random() * 4 + 2}px;
                    height: ${Math.random() * 4 + 2}px;
                    background: ${Math.random() > 0.5 ? '#ffd700' : '#4facfe'};
                    border-radius: 50%;
                    left: ${Math.random() * 100}%;
                    top: 100%;
                    opacity: ${Math.random() * 0.6 + 0.2};
                    animation: floatUp ${Math.random() * 10 + 15}s linear forwards;
                `;
                particleContainer.appendChild(particle);

                setTimeout(() => particle.remove(), 25000);
            }
        }, 2000);
    }

    setupCursorTrail() {
        let trail = [];
        const maxTrailLength = 10;

        document.addEventListener('mousemove', (e) => {
            // Add current position to trail
            trail.push({ x: e.clientX, y: e.clientY, time: Date.now() });

            // Remove old trail points
            trail = trail.filter(point => Date.now() - point.time < 1000);

            // Limit trail length
            if (trail.length > maxTrailLength) {
                trail.shift();
            }

            // Create trail particles occasionally
            if (Math.random() < 0.1) {
                this.createTrailParticle(e.clientX, e.clientY);
            }
        });
    }

    createTrailParticle(x, y) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 2px;
            height: 2px;
            background: rgba(255, 215, 0, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9997;
            left: ${x}px;
            top: ${y}px;
            animation: fadeOut 0.8s ease-out forwards;
        `;

        if (!document.getElementById('cursor-trail-style')) {
            const style = document.createElement('style');
            style.id = 'cursor-trail-style';
            style.textContent = `
                @keyframes fadeOut {
                    from { opacity: 0.6; transform: scale(1); }
                    to { opacity: 0; transform: scale(0); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(particle);
        setTimeout(() => particle.remove(), 800);
    }

    setupDynamicBackground() {
        // Randomly change background gradient intensity
        setInterval(() => {
            const mysticalBg = document.querySelector('.mystical-bg');
            if (mysticalBg) {
                const intensity = Math.random() * 0.1 + 0.05;
                mysticalBg.style.opacity = intensity;
            }
        }, 5000);
    }

    startPeriodicUpdates() {
        // Update every 30 seconds
        this.updateInterval = setInterval(() => {
            this.updateUserStats();
            this.checkForNotifications();
            this.updateOnlineStatus();
        }, 30000);

        // Update every 5 minutes
        this.longUpdateInterval = setInterval(() => {
            this.updateGuildInfo();
            this.updateExpeditions();
        }, 300000);
    }

    pauseUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        if (this.longUpdateInterval) {
            clearInterval(this.longUpdateInterval);
            this.longUpdateInterval = null;
        }
    }

    resumeUpdates() {
        if (!this.updateInterval) {
            this.startPeriodicUpdates();
        }
    }

    updateUserStats() {
        // This would typically fetch from server
        // For now, just simulate updates
        const spiritualPowerEl = document.querySelector('[data-spiritual-power]');
        if (spiritualPowerEl) {
            const currentPower = parseInt(spiritualPowerEl.textContent.replace(/[^\d]/g, ''));
            const newPower = currentPower + Math.floor(Math.random() * 10);
            this.animateNumberChange(spiritualPowerEl, newPower);
        }
    }

    animateNumberChange(element, newValue) {
        const currentValue = parseInt(element.textContent.replace(/[^\d]/g, '')) || 0;
        const duration = 1000;
        const steps = 30;
        const stepValue = (newValue - currentValue) / steps;
        let currentStep = 0;

        const animation = setInterval(() => {
            currentStep++;
            const value = Math.floor(currentValue + (stepValue * currentStep));
            element.textContent = value.toLocaleString();

            if (currentStep >= steps) {
                clearInterval(animation);
                element.textContent = newValue.toLocaleString();
            }
        }, duration / steps);
    }

    checkForNotifications() {
        // Simulate checking for new notifications
        if (Math.random() < 0.1) { // 10% chance
            const notifications = [
                { title: 'Tu Luyện Thành Công', message: 'Bạn đã tăng 50 điểm linh lực!', type: 'cultivation' },
                { title: 'Thành Viên Mới', message: 'Có thiên đạo mới gia nhập bang hội!', type: 'info' },
                { title: 'Đạo Lữ Sắp Bắt Đầu', message: 'Đạo lữ "Rừng Tre Xanh" sẽ bắt đầu trong 5 phút!', type: 'warning' }
            ];
            
            const randomNotification = notifications[Math.floor(Math.random() * notifications.length)];
            this.showNotification(randomNotification.title, randomNotification.message, randomNotification.type);
        }
    }

    updateOnlineStatus() {
        // Update online user count and status
        const onlineCountEl = document.querySelector('[data-online-count]');
        if (onlineCountEl) {
            const count = Math.floor(Math.random() * 50) + 20;
            onlineCountEl.textContent = count;
        }
    }

    updateGuildInfo() {
        // Update guild-related information
        console.log('Updating guild information...');
    }

    updateExpeditions() {
        // Update expedition status
        console.log('Updating expedition information...');
    }

    quickCultivate() {
        // Quick cultivation function
        const cultivateBtn = document.querySelector('[onclick*="cultivate"]');
        if (cultivateBtn) {
            cultivateBtn.click();
        } else {
            this.showNotification('Tu Luyện', 'Không thể tu luyện ở trang này!', 'warning');
        }
    }

    sendQuickMessage() {
        const chatInput = document.getElementById('messageInput');
        if (chatInput && chatInput.value.trim()) {
            const form = chatInput.closest('form');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    }

    handleResponsiveAdjustments() {
        // Adjust UI elements for different screen sizes
        const isMobile = window.innerWidth <= 768;
        const cards = document.querySelectorAll('.mystical-card');
        
        cards.forEach(card => {
            if (isMobile) {
                card.style.margin = '0.5rem 0';
            } else {
                card.style.margin = '';
            }
        });
    }

    // Utility functions
    formatNumber(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'T';
        } else if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        } else {
            return `${minutes}:${secs.toString().padStart(2, '0')}`;
        }
    }

    getCultivationStageColor(stage) {
        const colorMap = {
            'Luyện Khí': '#6c757d',
            'Trúc Cơ': '#007bff',
            'Kết Đan': '#ffc107',
            'Nguyên Anh': '#dc3545',
            'Hóa Thần': '#8e2de2',
            'Luyện Hư': '#20c997',
            'Hợp Thể': '#fd7e14',
            'Đại Thừa': '#e83e8c',
            'Độ Kiếp': '#6f42c1',
            'Tản Tiên': '#ffd700'
        };
        
        for (const [stageName, color] of Object.entries(colorMap)) {
            if (stage.includes(stageName)) {
                return color;
            }
        }
        return '#6c757d';
    }

    // API helper functions
    async makeRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Request failed:', error);
            this.showNotification('Lỗi', 'Có lỗi xảy ra khi kết nối với server!', 'error');
            throw error;
        }
    }

    // Initialize on page load
    static initialize() {
        document.addEventListener('DOMContentLoaded', () => {
            window.tuTienApp = new TuTienApp();
            console.log('Tu Tien App initialized successfully!');
        });
    }
}

// Auto-initialize
TuTienApp.initialize();

// Global utility functions
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading-spinner"></div>';
        element.disabled = true;
    }
}

function hideLoading(element, originalContent) {
    if (element) {
        element.innerHTML = originalContent;
        element.disabled = false;
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        if (window.tuTienApp) {
            window.tuTienApp.showNotification('Thành Công', 'Đã sao chép vào clipboard!', 'success');
        }
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

function formatCultivationLevel(level) {
    const stages = {
        'Luyện Khí': '练气',
        'Trúc Cơ': '筑基',
        'Kết Đan': '结丹',
        'Nguyên Anh': '元婴',
        'Hóa Thần': '化神',
        'Luyện Hư': '炼虚',
        'Hợp Thể': '合体',
        'Đại Thừa': '大乘',
        'Độ Kiếp': '渡劫',
        'Tản Tiên': '散仙'
    };
    
    for (const [vietnamese, chinese] of Object.entries(stages)) {
        if (level.includes(vietnamese)) {
            return level.replace(vietnamese, `${vietnamese} ${chinese}`);
        }
    }
    return level;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TuTienApp;
}
