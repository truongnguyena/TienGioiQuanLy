class AIAssistant {
    constructor() {
        this.isVisible = false;
        this.currentType = 'general';
        this.isLoading = false;
        this.init();
    }

    init() {
        this.createAssistantUI();
        this.setupEventListeners();
    }

    createAssistantUI() {
        // Create floating AI button
        const floatingBtn = document.createElement('div');
        floatingBtn.id = 'ai-floating-btn';
        floatingBtn.className = 'ai-floating-btn';
        floatingBtn.innerHTML = `
            <i class="fas fa-robot"></i>
            <span class="ai-btn-text">AI Hỗ Trợ</span>
        `;
        
        // Create AI assistant modal
        const assistantModal = document.createElement('div');
        assistantModal.id = 'ai-assistant-modal';
        assistantModal.className = 'modal fade';
        assistantModal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content bg-dark border-celestial">
                    <div class="modal-header border-celestial">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-robot text-celestial me-2"></i>
                            <h5 class="modal-title text-golden mb-0">Thiên Cơ Tiên Nhân - AI Hỗ Trợ Tu Tiên</h5>
                        </div>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <!-- AI Type Selection -->
                        <div class="ai-type-selection mb-3">
                            <div class="btn-group w-100" role="group">
                                <input type="radio" class="btn-check" name="ai-type" id="ai-cultivation" value="cultivation" checked>
                                <label class="btn btn-outline-celestial btn-sm" for="ai-cultivation">
                                    <i class="fas fa-fist-raised"></i> Tu Luyện
                                </label>
                                
                                <input type="radio" class="btn-check" name="ai-type" id="ai-guild" value="guild">
                                <label class="btn btn-outline-celestial btn-sm" for="ai-guild">
                                    <i class="fas fa-users"></i> Bang Hội
                                </label>
                                
                                <input type="radio" class="btn-check" name="ai-type" id="ai-expedition" value="expedition">
                                <label class="btn btn-outline-celestial btn-sm" for="ai-expedition">
                                    <i class="fas fa-map"></i> Đạo Lữ
                                </label>
                                
                                <input type="radio" class="btn-check" name="ai-type" id="ai-resource" value="resource">
                                <label class="btn btn-outline-celestial btn-sm" for="ai-resource">
                                    <i class="fas fa-gem"></i> Tài Nguyên
                                </label>
                                
                                <input type="radio" class="btn-check" name="ai-type" id="ai-general" value="general">
                                <label class="btn btn-outline-celestial btn-sm" for="ai-general">
                                    <i class="fas fa-question-circle"></i> Khác
                                </label>
                            </div>
                        </div>

                        <!-- Question Input (for general questions) -->
                        <div id="ai-question-input" class="mb-3" style="display: none;">
                            <label class="form-label text-light">Câu hỏi của bạn:</label>
                            <textarea class="form-control bg-dark text-light border-celestial" 
                                      id="ai-question" rows="3" 
                                      placeholder="Hỏi bất cứ điều gì về thế giới Tu Tiên..."></textarea>
                        </div>

                        <!-- Goals Input (for resource optimization) -->
                        <div id="ai-goals-input" class="mb-3" style="display: none;">
                            <label class="form-label text-light">Mục tiêu của bạn (tùy chọn):</label>
                            <input type="text" class="form-control bg-dark text-light border-celestial" 
                                   id="ai-goals" placeholder="VD: Tăng cảnh giới, Xây dựng bang hội...">
                        </div>

                        <!-- AI Response Area -->
                        <div class="ai-response-area">
                            <div id="ai-response-loading" class="text-center" style="display: none;">
                                <div class="spinner-border text-celestial" role="status">
                                    <span class="visually-hidden">Đang xử lý...</span>
                                </div>
                                <p class="text-light mt-2">Thiên Cơ Tiên Nhân đang suy ngẫm...</p>
                            </div>
                            
                            <div id="ai-response-content" class="ai-response-content" style="display: none;">
                                <div class="response-header">
                                    <i class="fas fa-robot text-celestial"></i>
                                    <span class="text-golden">Lời khuyên từ Thiên Cơ Tiên Nhân:</span>
                                </div>
                                <div id="ai-response-text" class="response-text"></div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer border-celestial">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                        <button type="button" class="btn btn-celestial" id="ai-ask-btn">
                            <i class="fas fa-paper-plane"></i> Hỏi Tiên Nhân
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(floatingBtn);
        document.body.appendChild(assistantModal);
        
        // Add CSS styles
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .ai-floating-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: linear-gradient(135deg, var(--celestial-primary), var(--celestial-secondary));
                color: white;
                border-radius: 50px;
                padding: 15px 20px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
                z-index: 1000;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                user-select: none;
            }
            
            .ai-floating-btn:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
            }
            
            .ai-floating-btn i {
                font-size: 1.2rem;
            }
            
            .ai-btn-text {
                font-size: 0.9rem;
                font-weight: 600;
            }
            
            @media (max-width: 768px) {
                .ai-btn-text {
                    display: none;
                }
                .ai-floating-btn {
                    padding: 15px;
                    border-radius: 50%;
                }
            }
            
            .ai-response-content {
                background: rgba(138, 43, 226, 0.1);
                border: 1px solid var(--celestial-primary);
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
            }
            
            .response-header {
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .response-text {
                color: var(--text-light);
                line-height: 1.6;
                white-space: pre-wrap;
                max-height: 300px;
                overflow-y: auto;
            }
            
            .ai-type-selection .btn {
                font-size: 0.8rem;
            }
            
            .btn-check:checked + .btn-outline-celestial {
                background-color: var(--celestial-primary);
                border-color: var(--celestial-primary);
                color: white;
            }
        `;
        document.head.appendChild(style);
    }

    setupEventListeners() {
        // Floating button click
        document.getElementById('ai-floating-btn').addEventListener('click', () => {
            this.showAssistant();
        });

        // AI type selection
        document.querySelectorAll('input[name="ai-type"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentType = e.target.value;
                this.updateInputFields();
            });
        });

        // Ask button click
        document.getElementById('ai-ask-btn').addEventListener('click', () => {
            this.getAIAdvice();
        });

        // Enter key in question input
        document.getElementById('ai-question').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.getAIAdvice();
            }
        });
    }

    showAssistant() {
        const modal = new bootstrap.Modal(document.getElementById('ai-assistant-modal'));
        modal.show();
        this.updateInputFields();
    }

    updateInputFields() {
        const questionInput = document.getElementById('ai-question-input');
        const goalsInput = document.getElementById('ai-goals-input');
        
        // Hide all inputs first
        questionInput.style.display = 'none';
        goalsInput.style.display = 'none';
        
        // Show appropriate inputs
        if (this.currentType === 'general') {
            questionInput.style.display = 'block';
        } else if (this.currentType === 'resource') {
            goalsInput.style.display = 'block';
        }
    }

    async getAIAdvice() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading();
        
        try {
            let endpoint = '';
            let data = {};
            
            switch (this.currentType) {
                case 'cultivation':
                    endpoint = '/api/ai/cultivation-advice';
                    break;
                case 'guild':
                    endpoint = '/api/ai/guild-management';
                    break;
                case 'expedition':
                    endpoint = '/api/ai/expedition-advice';
                    break;
                case 'resource':
                    endpoint = '/api/ai/resource-optimization';
                    const goals = document.getElementById('ai-goals').value.trim();
                    data = { goals: goals ? goals.split(',').map(g => g.trim()) : [] };
                    break;
                case 'general':
                    endpoint = '/api/ai/general';
                    const question = document.getElementById('ai-question').value.trim();
                    if (!question) {
                        this.showError('Vui lòng nhập câu hỏi!');
                        return;
                    }
                    data = { question };
                    break;
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showResponse(result.advice, this.currentType);
            } else {
                this.showError(result.error || 'Đã xảy ra lỗi không mong muốn!');
            }
            
        } catch (error) {
            console.error('AI Assistant Error:', error);
            this.showError('Không thể kết nối với Thiên Cơ Tiên Nhân. Vui lòng thử lại sau!');
        } finally {
            this.isLoading = false;
            this.hideLoading();
        }
    }

    showLoading() {
        document.getElementById('ai-response-loading').style.display = 'block';
        document.getElementById('ai-response-content').style.display = 'none';
        document.getElementById('ai-ask-btn').disabled = true;
    }

    hideLoading() {
        document.getElementById('ai-response-loading').style.display = 'none';
        document.getElementById('ai-ask-btn').disabled = false;
    }

    showResponse(advice, type) {
        document.getElementById('ai-response-text').textContent = advice;
        document.getElementById('ai-response-content').style.display = 'block';
        
        // Scroll to response
        document.getElementById('ai-response-content').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    }

    showError(message) {
        document.getElementById('ai-response-text').textContent = `❌ ${message}`;
        document.getElementById('ai-response-content').style.display = 'block';
    }
}

// Initialize AI Assistant when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (typeof window.tuTienApp !== 'undefined' || document.querySelector('.dashboard-container')) {
        window.aiAssistant = new AIAssistant();
    }
});