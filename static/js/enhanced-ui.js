// Enhanced UI JavaScript for Tu Tien Community
class EnhancedUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollEffects();
        this.setupSocialLinks();
        this.setupAnimations();
        this.setupMobileOptimizations();
        this.setupLoadingStates();
    }

    setupScrollEffects() {
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Parallax effect for hero section
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const heroSection = document.querySelector('.hero-section');
            if (heroSection) {
                heroSection.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
    }

    setupSocialLinks() {
        // Add click tracking for social links
        document.querySelectorAll('.social-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const platform = link.querySelector('i').className;
                console.log(`Social link clicked: ${platform}`);
                
                // Add visual feedback
                link.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    link.style.transform = '';
                }, 150);
            });
        });
    }

    setupAnimations() {
        // Intersection Observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                }
            });
        }, observerOptions);

        // Observe all feature cards and stats
        document.querySelectorAll('.feature-card, .stat-item, .mystical-card').forEach(el => {
            observer.observe(el);
        });
    }

    setupMobileOptimizations() {
        // Touch-friendly interactions
        document.querySelectorAll('.btn, .nav-link').forEach(element => {
            element.addEventListener('touchstart', function() {
                this.classList.add('touch-active');
            });
            
            element.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.classList.remove('touch-active');
                }, 150);
            });
        });

        // Mobile menu enhancements
        const mobileMenuToggle = document.querySelector('[data-bs-toggle="offcanvas"]');
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', () => {
                document.body.classList.toggle('menu-open');
            });
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            const sidebar = document.querySelector('.mystical-sidebar');
            const toggle = document.querySelector('[data-bs-toggle="offcanvas"]');
            
            if (sidebar && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                if (sidebar.classList.contains('show')) {
                    const bsOffcanvas = bootstrap.Offcanvas.getInstance(sidebar);
                    if (bsOffcanvas) {
                        bsOffcanvas.hide();
                    }
                }
            }
        });
    }

    setupLoadingStates() {
        // Add loading states to forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                }
            });
        });

        // Add loading states to links that might take time
        document.querySelectorAll('a[href*="dashboard"], a[href*="mining"]').forEach(link => {
            link.addEventListener('click', function() {
                this.classList.add('loading');
            });
        });
    }

    // Utility method to show notifications
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Method to enhance cards with hover effects
    enhanceCards() {
        document.querySelectorAll('.mystical-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedUI();
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .touch-active {
        transform: scale(0.95);
        opacity: 0.8;
    }
    
    .menu-open {
        overflow: hidden;
    }
    
    .mystical-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .social-link {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .btn-mystical {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .loading {
        position: relative;
        pointer-events: none;
        opacity: 0.7;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 20px;
        height: 20px;
        margin: -10px 0 0 -10px;
        border: 2px solid #ffd700;
        border-top: 2px solid transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);