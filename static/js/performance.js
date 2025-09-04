// Performance optimization utilities
class PerformanceOptimizer {
    constructor() {
        this.cache = new Map();
        this.requestQueue = new Set();
        this.init();
    }
    
    init() {
        // Preload critical resources
        this.preloadCriticalAssets();
        
        // Setup lazy loading for images
        this.setupLazyLoading();
        
        // Optimize API calls
        this.setupAPIOptimization();
        
        // Setup smooth scrolling
        this.setupSmoothScrolling();
    }
    
    preloadCriticalAssets() {
        const criticalAssets = [
            '/static/css/style.css',
            '/static/js/main.js'
        ];
        
        criticalAssets.forEach(asset => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = asset;
            link.as = asset.endsWith('.css') ? 'style' : 'script';
            document.head.appendChild(link);
        });
    }
    
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                            observer.unobserve(img);
                        }
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                observer.observe(img);
            });
        }
    }
    
    setupAPIOptimization() {
        // Debounce function for API calls
        this.debounce = (func, wait) => {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        };
        
        // Cache API responses
        this.cacheResponse = (key, data, ttl = 300000) => { // 5 minutes default
            this.cache.set(key, {
                data: data,
                timestamp: Date.now(),
                ttl: ttl
            });
        };
        
        this.getCachedResponse = (key) => {
            const cached = this.cache.get(key);
            if (cached && (Date.now() - cached.timestamp < cached.ttl)) {
                return cached.data;
            }
            this.cache.delete(key);
            return null;
        };
    }
    
    setupSmoothScrolling() {
        // Enable smooth scrolling for all anchor links
        document.addEventListener('click', (e) => {
            if (e.target.matches('a[href^="#"]')) {
                e.preventDefault();
                const target = document.querySelector(e.target.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    }
    
    // Optimize form submissions
    optimizeFormSubmission(formElement, callback) {
        const submitBtn = formElement.querySelector('button[type="submit"]');
        
        formElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Prevent double submission
            if (this.requestQueue.has(formElement)) {
                return;
            }
            
            this.requestQueue.add(formElement);
            
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang xử lý...';
                
                try {
                    await callback(new FormData(formElement));
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                    this.requestQueue.delete(formElement);
                }
            }
        });
    }
    
    // Add loading states to buttons
    addLoadingState(button, promise) {
        const originalText = button.textContent;
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Đang tải...';
        
        promise.finally(() => {
            button.disabled = false;
            button.textContent = originalText;
        });
    }
    
    // Virtualize long lists for better performance
    virtualizeList(container, items, renderItem, itemHeight = 50) {
        const viewport = container.parentElement;
        const visibleItems = Math.ceil(viewport.clientHeight / itemHeight) + 2;
        let startIndex = 0;
        
        const render = () => {
            container.innerHTML = '';
            container.style.height = `${items.length * itemHeight}px`;
            
            const fragment = document.createDocumentFragment();
            
            for (let i = startIndex; i < Math.min(startIndex + visibleItems, items.length); i++) {
                const item = renderItem(items[i], i);
                item.style.position = 'absolute';
                item.style.top = `${i * itemHeight}px`;
                item.style.width = '100%';
                fragment.appendChild(item);
            }
            
            container.appendChild(fragment);
        };
        
        viewport.addEventListener('scroll', this.debounce(() => {
            startIndex = Math.floor(viewport.scrollTop / itemHeight);
            render();
        }, 16)); // ~60fps
        
        render();
    }
}

// Initialize performance optimizer
const perfOptimizer = new PerformanceOptimizer();

// Export for use in other modules
window.perfOptimizer = perfOptimizer;