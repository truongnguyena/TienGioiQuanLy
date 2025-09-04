// Enhanced UI Management System
class EnhancedUI {
    constructor() {
        this.loadingElements = new Set();
        this.notificationQueue = [];
        this.init();
    }

    init() {
        this.setupGlobalErrorHandling();
        this.setupLoadingStates();
        this.setupNotifications();
        this.setupFormValidation();
        this.setupResponsiveFeatures();
    }

    // Global Error Handling
    setupGlobalErrorHandling() {
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            this.showNotification('Đã xảy ra lỗi không mong muốn', 'error');
        });

        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.showNotification('Lỗi kết nối mạng', 'error');
        });
    }

    // Loading States Management
    setupLoadingStates() {
        // Intercept fetch requests to show loading
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            const url = args[0];
            if (typeof url === 'string' && url.startsWith('/')) {
                this.showLoading();
            }
            
            try {
                const response = await originalFetch(...args);
                this.hideLoading();
                return response;
            } catch (error) {
                this.hideLoading();
                throw error;
            }
        };
    }

    showLoading(element = null) {
        if (element) {
            element.classList.add('loading');
            this.loadingElements.add(element);
        } else {
            document.body.classList.add('loading');
        }
    }

    hideLoading(element = null) {
        if (element) {
            element.classList.remove('loading');
            this.loadingElements.delete(element);
        } else {
            document.body.classList.remove('loading');
        }
    }

    // Notification System
    setupNotifications() {
        // Create notification container
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
    }

    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        
        const typeClasses = {
            'success': 'success-message',
            'error': 'error-message',
            'warning': 'warning-message',
            'info': 'info-message'
        };

        notification.className = `notification ${typeClasses[type] || 'info-message'}`;
        notification.style.cssText = `
            margin-bottom: 10px;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideInRight 0.3s ease-out;
            position: relative;
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; color: inherit; cursor: pointer; font-size: 18px;">
                    ×
                </button>
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
    }

    // Form Validation
    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'Trường này là bắt buộc');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }

            // Email validation
            if (input.type === 'email' && input.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(input.value)) {
                    this.showFieldError(input, 'Email không hợp lệ');
                    isValid = false;
                }
            }

            // Password validation
            if (input.type === 'password' && input.value) {
                if (input.value.length < 6) {
                    this.showFieldError(input, 'Mật khẩu phải có ít nhất 6 ký tự');
                    isValid = false;
                }
            }
        });

        return isValid;
    }

    showFieldError(input, message) {
        input.classList.add('is-invalid');
        
        let errorElement = input.parentElement.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            input.parentElement.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    clearFieldError(input) {
        input.classList.remove('is-invalid');
        const errorElement = input.parentElement.querySelector('.invalid-feedback');
        if (errorElement) {
            errorElement.remove();
        }
    }

    // Responsive Features
    setupResponsiveFeatures() {
        // Mobile menu toggle
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuToggle && mobileMenu) {
            mobileMenuToggle.addEventListener('click', () => {
                mobileMenu.classList.toggle('show');
            });
        }

        // Touch gestures for mobile
        this.setupTouchGestures();
    }

    setupTouchGestures() {
        let startY = 0;
        let startX = 0;

        document.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
            startX = e.touches[0].clientX;
        });

        document.addEventListener('touchmove', (e) => {
            if (!startY || !startX) return;

            const currentY = e.touches[0].clientY;
            const currentX = e.touches[0].clientX;
            const diffY = startY - currentY;
            const diffX = startX - currentX;

            // Swipe up to refresh
            if (Math.abs(diffY) > Math.abs(diffX) && diffY > 50) {
                this.handleSwipeUp();
            }
        });
    }

    handleSwipeUp() {
        // Refresh page on swipe up
        if (window.location.pathname === '/') {
            window.location.reload();
        }
    }

    // Utility Methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Animation helpers
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.display = 'block';
        
        let start = performance.now();
        
        function animate(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    }

    fadeOut(element, duration = 300) {
        let start = performance.now();
        const initialOpacity = parseFloat(getComputedStyle(element).opacity);
        
        function animate(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = initialOpacity * (1 - progress);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.display = 'none';
            }
        }
        
        requestAnimationFrame(animate);
    }
}

// Initialize Enhanced UI
document.addEventListener('DOMContentLoaded', () => {
    window.enhancedUI = new EnhancedUI();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .is-invalid {
        border-color: #dc3545 !important;
    }
    
    .invalid-feedback {
        display: block;
        color: #dc3545;
        font-size: 0.875rem;
        margin-top: 0.25rem;
    }
    
    .warning-message {
        background: rgba(255, 193, 7, 0.1);
        border: 1px solid rgba(255, 193, 7, 0.3);
        color: #ffc107;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .info-message {
        background: rgba(13, 202, 240, 0.1);
        border: 1px solid rgba(13, 202, 240, 0.3);
        color: #0dcaf0;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
`;
document.head.appendChild(style);
