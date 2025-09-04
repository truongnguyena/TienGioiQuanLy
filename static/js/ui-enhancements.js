// UI/UX Enhancement Module
class UIEnhancer {
    constructor() {
        this.init();
    }
    
    init() {
        this.addSmoothAnimations();
        this.enhanceTooltips();
        this.addProgressIndicators();
        this.improveFormValidation();
        this.addConfirmationDialogs();
        this.enhanceNotifications();
    }
    
    addSmoothAnimations() {
        // Add fade-in animation to newly added elements
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1 && !node.classList.contains('no-animate')) {
                        node.style.opacity = '0';
                        node.style.transform = 'translateY(10px)';
                        setTimeout(() => {
                            node.style.transition = 'all 0.3s ease-out';
                            node.style.opacity = '1';
                            node.style.transform = 'translateY(0)';
                        }, 10);
                    }
                });
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    enhanceTooltips() {
        // Initialize Bootstrap tooltips with custom styling
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip, {
                customClass: 'mystical-tooltip',
                delay: { show: 300, hide: 100 }
            });
        });
    }
    
    addProgressIndicators() {
        // Add progress indicators for cultivation advancement
        const progressBars = document.querySelectorAll('.cultivation-progress');
        progressBars.forEach(bar => {
            const progress = parseFloat(bar.dataset.progress) || 0;
            const progressBar = bar.querySelector('.progress-bar');
            
            if (progressBar) {
                // Animate progress bar
                setTimeout(() => {
                    progressBar.style.width = `${progress}%`;
                    progressBar.style.transition = 'width 1s ease-out';
                }, 100);
                
                // Add glow effect when near completion
                if (progress > 80) {
                    progressBar.classList.add('glow-effect');
                }
            }
        });
    }
    
    improveFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
                
                input.addEventListener('input', () => {
                    if (input.classList.contains('is-invalid')) {
                        this.validateField(input);
                    }
                });
            });
        });
    }
    
    validateField(field) {
        let isValid = true;
        let message = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !field.value.trim()) {
            isValid = false;
            message = 'Trường này là bắt buộc';
        }
        
        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                isValid = false;
                message = 'Địa chỉ email không hợp lệ';
            }
        }
        
        // Number validation
        if (field.type === 'number' && field.value) {
            const min = parseFloat(field.getAttribute('min'));
            const max = parseFloat(field.getAttribute('max'));
            const value = parseFloat(field.value);
            
            if (!isNaN(min) && value < min) {
                isValid = false;
                message = `Giá trị phải lớn hơn hoặc bằng ${min}`;
            }
            
            if (!isNaN(max) && value > max) {
                isValid = false;
                message = `Giá trị phải nhỏ hơn hoặc bằng ${max}`;
            }
        }
        
        this.updateFieldValidation(field, isValid, message);
    }
    
    updateFieldValidation(field, isValid, message) {
        const feedbackElement = field.parentElement.querySelector('.invalid-feedback') || 
                               this.createFeedbackElement(field.parentElement);
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            feedbackElement.textContent = '';
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            feedbackElement.textContent = message;
        }
    }
    
    createFeedbackElement(parent) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        parent.appendChild(feedback);
        return feedback;
    }
    
    addConfirmationDialogs() {
        // Add confirmation for destructive actions
        const destructiveActions = document.querySelectorAll('[data-confirm]');
        destructiveActions.forEach(element => {
            element.addEventListener('click', (e) => {
                const message = element.dataset.confirm;
                if (!confirm(message)) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });
    }
    
    enhanceNotifications() {
        // Auto-hide success notifications
        const alerts = document.querySelectorAll('.alert-success');
        alerts.forEach(alert => {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.style.transition = 'opacity 0.5s ease-out';
                    alert.style.opacity = '0';
                    setTimeout(() => {
                        if (alert.parentNode) {
                            alert.remove();
                        }
                    }, 500);
                }
            }, 3000);
        });
        
        // Add sound effects for notifications (optional)
        if (localStorage.getItem('soundEnabled') === 'true') {
            this.addNotificationSounds();
        }
    }
    
    addNotificationSounds() {
        // Create audio context for sound effects
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        const playSound = (frequency, duration) => {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = frequency;
            oscillator.type = 'sine';
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + duration);
        };
        
        // Success sound
        document.addEventListener('DOMContentLoaded', () => {
            const successAlerts = document.querySelectorAll('.alert-success');
            successAlerts.forEach(() => {
                playSound(523.25, 0.3); // C5 note
            });
        });
        
        // Error sound
        document.addEventListener('DOMContentLoaded', () => {
            const errorAlerts = document.querySelectorAll('.alert-danger');
            errorAlerts.forEach(() => {
                playSound(220, 0.5); // A3 note
            });
        });
    }
    
    // Add mystical particle effects
    addParticleEffects() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particle-container';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
        `;
        document.body.appendChild(particleContainer);
        
        const createParticle = (x, y) => {
            const particle = document.createElement('div');
            particle.className = 'mystical-particle';
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: linear-gradient(45deg, #ffd700, #ff6b35);
                border-radius: 50%;
                pointer-events: none;
                left: ${x}px;
                top: ${y}px;
                animation: float-up 2s ease-out forwards;
            `;
            
            particleContainer.appendChild(particle);
            
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.remove();
                }
            }, 2000);
        };
        
        // Create particles on successful actions
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-success') || 
                e.target.closest('.btn-success')) {
                for (let i = 0; i < 5; i++) {
                    setTimeout(() => {
                        createParticle(
                            e.clientX + (Math.random() - 0.5) * 100,
                            e.clientY + (Math.random() - 0.5) * 100
                        );
                    }, i * 100);
                }
            }
        });
    }
}

// CSS animations for particles
const style = document.createElement('style');
style.textContent = `
    @keyframes float-up {
        0% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        100% {
            opacity: 0;
            transform: translateY(-100px) scale(0);
        }
    }
    
    .glow-effect {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        }
        50% {
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.9);
        }
    }
    
    .mystical-tooltip .tooltip-inner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 1px solid #ffd700;
        font-size: 0.875rem;
    }
    
    .mystical-tooltip .tooltip-arrow::before {
        border-top-color: #667eea;
    }
`;
document.head.appendChild(style);

// Initialize UI enhancer
const uiEnhancer = new UIEnhancer();
uiEnhancer.addParticleEffects();

// Export for global use
window.uiEnhancer = uiEnhancer;