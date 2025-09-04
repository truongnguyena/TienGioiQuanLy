// Guild Management JavaScript functionality
class GuildManager {
    constructor() {
        this.currentGuild = null;
        this.warPredictions = [];
        this.memberUpdateTimer = null;
        this.init();
    }

    init() {
        this.setupGuildActions();
        this.setupWarSystem();
        this.setupMemberManagement();
        this.setupAIIntegration();
        this.startGuildUpdates();
    }

    setupGuildActions() {
        // Guild creation form handling
        const createGuildForm = document.getElementById('createGuildForm');
        if (createGuildForm) {
            createGuildForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleGuildCreation();
            });
        }

        // Guild settings
        const guildSettingsForm = document.getElementById('guildSettingsForm');
        if (guildSettingsForm) {
            guildSettingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.updateGuildSettings();
            });
        }

        // Guild recruitment toggle
        const recruitmentToggle = document.getElementById('recruitmentToggle');
        if (recruitmentToggle) {
            recruitmentToggle.addEventListener('change', (e) => {
                this.toggleRecruitment(e.target.checked);
            });
        }
    }

    async handleGuildCreation() {
        const form = document.getElementById('createGuildForm');
        if (!form) {
            console.error('Guild creation form not found');
            return;
        }

        const formData = new FormData(form);
        
        const guildData = {
            name: formData.get('name'),
            description: formData.get('description')
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.innerHTML : '';
        if (submitBtn) {
            showLoading(submitBtn);
        }

        try {
            const response = await fetch('/api/create-guild', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(guildData)
            });

            const data = await response.json();

            if (data.success) {
                window.tuTienApp.showNotification(
                    'Bang Hội Thành Lập!', 
                    data.message, 
                    'success'
                );
                
                // Close modal and refresh page
                closeCreateGuildModal();
                
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                throw new Error(data.error || 'Không thể tạo bang hội');
            }
        } catch (error) {
            console.error('Guild creation error:', error);
            window.tuTienApp.showNotification('Lỗi Tạo Bang Hội', error.message, 'error');
        } finally {
            if (submitBtn) {
                hideLoading(submitBtn, originalText);
            }
        }
    }

    async updateGuildSettings() {
        const form = document.getElementById('guildSettingsForm');
        const formData = new FormData(form);
        
        const settings = {
            description: formData.get('description'),
            recruitment_open: formData.get('recruitment_open') === 'on',
            min_cultivation_level: formData.get('min_cultivation_level')
        };

        try {
            const response = await fetch('/api/update-guild-settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(settings)
            });

            const data = await response.json();

            if (data.success) {
                window.tuTienApp.showNotification('Cập Nhật Thành Công', 'Cài đặt bang hội đã được lưu', 'success');
                const modal = bootstrap.Modal.getInstance(document.getElementById('guildSettingsModal'));
                modal?.hide();
            } else {
                throw new Error(data.error || 'Không thể cập nhật cài đặt');
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi Cập Nhật', error.message, 'error');
        }
    }

    async toggleRecruitment(isOpen) {
        try {
            const response = await fetch('/api/toggle-guild-recruitment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ recruitment_open: isOpen })
            });

            const data = await response.json();

            if (data.success) {
                const status = isOpen ? 'mở' : 'đóng';
                window.tuTienApp.showNotification(
                    'Tuyển Thành Viên', 
                    `Đã ${status} tuyển thành viên`, 
                    'info'
                );
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    setupWarSystem() {
        // War declaration form
        const declareWarForm = document.getElementById('declareWarForm');
        if (declareWarForm) {
            declareWarForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleWarDeclaration();
            });
        }

        // War prediction refresh
        const refreshPredictionsBtn = document.getElementById('refreshWarPredictions');
        if (refreshPredictionsBtn) {
            refreshPredictionsBtn.addEventListener('click', () => {
                this.refreshWarPredictions();
            });
        }
    }

    async handleWarDeclaration() {
        const form = document.getElementById('declareWarForm');
        const formData = new FormData(form);
        
        const warData = {
            target_guild_id: formData.get('target_guild_id'),
            war_type: formData.get('war_type')
        };

        if (!warData.target_guild_id || !warData.war_type) {
            window.tuTienApp.showNotification('Lỗi', 'Vui lòng điền đầy đủ thông tin!', 'warning');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn ? submitBtn.innerHTML : '';
        if (submitBtn) {
            showLoading(submitBtn);
        }

        try {
            const response = await fetch('/api/declare-war', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(warData)
            });

            const data = await response.json();

            if (data.success) {
                this.showWarDeclarationEffect(warData.war_type);
                window.tuTienApp.showNotification(
                    'Tuyên Chiến Thành Công!', 
                    `Đã tuyên ${warData.war_type} với bang hội mục tiêu`, 
                    'warning'
                );
                
                // Close modal and refresh
                const modal = bootstrap.Modal.getInstance(document.getElementById('declareWarModal'));
                modal.hide();
                
                setTimeout(() => {
                    location.reload();
                }, 2000);
            } else {
                throw new Error(data.error || 'Không thể tuyên chiến');
            }
        } catch (error) {
            console.error('War declaration error:', error);
            window.tuTienApp.showNotification('Lỗi Tuyên Chiến', error.message, 'error');
        } finally {
            if (submitBtn) {
                hideLoading(submitBtn, originalText);
            }
        }
    }

    showWarDeclarationEffect(warType) {
        // Create dramatic war declaration effect
        const effect = document.createElement('div');
        effect.className = 'war-declaration-effect';
        effect.innerHTML = `
            <div class="war-effect-content">
                <h1 class="war-title">⚔️ TUYÊN CHIẾN! ⚔️</h1>
                <h2 class="war-type">${warType}</h2>
                <div class="war-flames"></div>
            </div>
        `;
        effect.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(220, 53, 69, 0.4), rgba(0, 0, 0, 0.8));
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: warDeclarationFade 3s ease-out forwards;
        `;

        // Add war effect styles
        if (!document.getElementById('war-effects-style')) {
            const style = document.createElement('style');
            style.id = 'war-effects-style';
            style.textContent = `
                @keyframes warDeclarationFade {
                    0% { opacity: 0; }
                    20% { opacity: 1; }
                    80% { opacity: 1; }
                    100% { opacity: 0; }
                }
                .war-title {
                    color: #dc3545;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                    font-size: 3rem;
                    margin-bottom: 1rem;
                    animation: shake 0.5s infinite;
                }
                .war-type {
                    color: #ffd700;
                    font-size: 2rem;
                    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-5px); }
                    75% { transform: translateX(5px); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(effect);
        
        // Auto remove after animation
        setTimeout(() => effect.remove(), 3000);

        // Play war sound effect
        this.playWarSound();
    }

    playWarSound() {
        // Create dramatic war sound
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            const audioContext = new (AudioContext || webkitAudioContext)();
            
            // Create a more complex war sound
            const oscillator1 = audioContext.createOscillator();
            const oscillator2 = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator1.connect(gainNode);
            oscillator2.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator1.frequency.setValueAtTime(220, audioContext.currentTime);
            oscillator2.frequency.setValueAtTime(110, audioContext.currentTime);
            
            oscillator1.frequency.exponentialRampToValueAtTime(440, audioContext.currentTime + 0.3);
            oscillator2.frequency.exponentialRampToValueAtTime(220, audioContext.currentTime + 0.3);
            
            gainNode.gain.setValueAtTime(0.4, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1.5);

            oscillator1.start(audioContext.currentTime);
            oscillator1.stop(audioContext.currentTime + 1.5);
            oscillator2.start(audioContext.currentTime);
            oscillator2.stop(audioContext.currentTime + 1.5);
        }
    }

    async refreshWarPredictions() {
        const container = document.querySelector('.war-predictions-container');
        if (!container) return;

        container.innerHTML = '<div class="text-center"><div class="loading-spinner"></div><p class="text-light mt-2">AI đang phân tích chiến lực...</p></div>';

        try {
            const response = await fetch('/api/refresh-war-predictions', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.renderWarPredictions(data.predictions);
                window.tuTienApp.showNotification('AI Phân Tích', 'Đã cập nhật dự đoán chiến tranh!', 'info');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            container.innerHTML = '<p class="text-danger">Không thể tải dự đoán chiến tranh</p>';
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    renderWarPredictions(predictions) {
        const container = document.querySelector('.war-predictions-container');
        if (!container) return;

        container.innerHTML = predictions.map(prediction => `
            <div class="col-lg-4 mb-3">
                <div class="prediction-card">
                    <h6 class="text-purple">${prediction.target_guild_name}</h6>
                    <div class="prediction-stats">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="text-light">Tỷ Lệ Thắng:</span>
                            <span class="text-${prediction.win_probability > 60 ? 'success' : prediction.win_probability > 40 ? 'warning' : 'danger'}">
                                ${prediction.win_probability}%
                            </span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                            <span class="text-light">Thời Gian Dự Kiến:</span>
                            <span class="text-celestial">${prediction.duration_days} ngày</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span class="text-light">Tổn Thất:</span>
                            <span class="text-${prediction.casualty_estimate === 'Cao' ? 'danger' : 'warning'}">
                                ${prediction.casualty_estimate}
                            </span>
                        </div>
                    </div>
                    <div class="prediction-actions mt-3">
                        <button class="btn btn-sm btn-outline-purple mystical-btn w-100" 
                                onclick="guildManager.declareWarAgainst('${prediction.target_guild_id}', '${prediction.target_guild_name}')">
                            <i class="fas fa-sword me-1"></i>Tuyên Chiến
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    setupMemberManagement() {
        // Member promotion/demotion
        this.setupMemberActions();
        
        // Member kick functionality
        this.setupMemberKick();
        
        // Join request handling
        this.setupJoinRequests();
    }

    setupMemberActions() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="promote"]')) {
                const memberId = e.target.dataset.memberId;
                this.promoteMember(memberId);
            }
            
            if (e.target.matches('[data-action="demote"]')) {
                const memberId = e.target.dataset.memberId;
                this.demoteMember(memberId);
            }
            
            if (e.target.matches('[data-action="kick"]')) {
                const memberId = e.target.dataset.memberId;
                const memberName = e.target.dataset.memberName;
                this.kickMember(memberId, memberName);
            }
        });
    }

    async promoteMember(memberId) {
        if (!confirm('Bạn có chắc muốn thăng chức cho thành viên này?')) return;

        try {
            const response = await fetch('/api/promote-member', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ member_id: memberId })
            });

            const data = await response.json();

            if (data.success) {
                window.tuTienApp.showNotification('Thăng Chức', 'Đã thăng chức thành viên!', 'success');
                this.refreshMemberList();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    setupMemberKick() {
        // Member kick functionality is handled by setupMemberActions
        // This function is required but the logic is in setupMemberActions
    }

    async demoteMember(memberId) {
        if (!confirm('Bạn có chắc muốn giáng chức cho thành viên này?')) return;

        try {
            const response = await fetch('/api/demote-member', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ member_id: memberId })
            });

            const data = await response.json();

            if (data.success) {
                window.tuTienApp.showNotification('Giáng Chức', 'Đã giáng chức thành viên!', 'warning');
                this.refreshMemberList();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    async kickMember(memberId, memberName) {
        if (!confirm(`Bạn có chắc muốn đuổi ${memberName} khỏi bang hội?`)) return;

        try {
            const response = await fetch('/api/kick-member', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ member_id: memberId })
            });

            const data = await response.json();

            if (data.success) {
                window.tuTienApp.showNotification('Đuổi Thành Viên', `Đã đuổi ${memberName} khỏi bang hội!`, 'warning');
                this.refreshMemberList();
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    setupJoinRequests() {
        const joinRequestsContainer = document.getElementById('joinRequestsContainer');
        if (joinRequestsContainer) {
            this.loadJoinRequests();
        }
    }

    async loadJoinRequests() {
        try {
            const response = await fetch('/api/guild-join-requests', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.renderJoinRequests(data.requests);
            }
        } catch (error) {
            console.error('Failed to load join requests:', error);
        }
    }

    renderJoinRequests(requests) {
        const container = document.getElementById('joinRequestsContainer');
        if (!container) return;

        if (requests.length === 0) {
            container.innerHTML = '<p class="text-muted">Không có yêu cầu gia nhập nào</p>';
            return;
        }

        container.innerHTML = requests.map(request => `
            <div class="join-request-item mb-2">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong class="text-golden">${request.user_name}</strong>
                        <small class="text-muted d-block">${request.cultivation_level}</small>
                        <small class="text-celestial">${request.spiritual_power} Linh Lực</small>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-success mystical-btn me-2" 
                                onclick="guildManager.handleJoinRequest(${request.id}, true)">
                            <i class="fas fa-check"></i>
                        </button>
                        <button class="btn btn-sm btn-danger mystical-btn" 
                                onclick="guildManager.handleJoinRequest(${request.id}, false)">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async handleJoinRequest(requestId, accept) {
        try {
            const response = await fetch('/api/handle-join-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ 
                    request_id: requestId, 
                    accept: accept 
                })
            });

            const data = await response.json();

            if (data.success) {
                const action = accept ? 'chấp nhận' : 'từ chối';
                window.tuTienApp.showNotification('Yêu Cầu Gia Nhập', `Đã ${action} yêu cầu!`, accept ? 'success' : 'info');
                this.loadJoinRequests();
                if (accept) {
                    this.refreshMemberList();
                }
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            window.tuTienApp.showNotification('Lỗi', error.message, 'error');
        }
    }

    setupAIIntegration() {
        // AI guild strategy advisor
        const aiStrategyBtn = document.getElementById('aiStrategyBtn');
        if (aiStrategyBtn) {
            aiStrategyBtn.addEventListener('click', () => {
                this.openAIStrategy();
            });
        }

        // Guild performance analytics
        this.setupGuildAnalytics();
    }

    openAIStrategy() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content mystical-modal">
                    <div class="modal-header border-bottom border-secondary">
                        <h5 class="modal-title text-golden">
                            <i class="fas fa-chess me-2"></i>AI Chiến Thuật Bang Hội
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="ai-strategy-container">
                            <div class="text-center">
                                <div class="loading-spinner"></div>
                                <p class="text-light mt-2">AI đang phân tích tình hình bang hội...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();

        // Generate AI strategy
        this.generateAIStrategy(modal);

        // Clean up on close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    async generateAIStrategy(modal) {
        try {
            // Simulate AI analysis
            await new Promise(resolve => setTimeout(resolve, 2000));

            const strategies = [
                {
                    title: "Tăng Cường Tuyển Dụng",
                    description: "Bang hội cần thêm thành viên mạnh. Nên hạ thấp yêu cầu tuyển dụng và tích cực tìm kiếm tài năng.",
                    priority: "Cao",
                    impact: "Tăng 30% sức mạnh tổng thể"
                },
                {
                    title: "Phát Triển Kinh Tế",
                    description: "Tập trung vào các hoạt động tăng kho bạc bang hội. Khuyến khích thành viên đóng góp tài nguyên.",
                    priority: "Trung Bình",
                    impact: "Tăng 50% kho bạc trong 1 tháng"
                },
                {
                    title: "Mở Rộng Lãnh Thổ",
                    description: "Thời điểm tốt để chinh phục thêm lãnh thổ. Có thể tuyên chiến với bang hội yếu hơn.",
                    priority: "Thấp",
                    impact: "Tăng 2-3 lãnh thổ mới"
                }
            ];

            const container = modal.querySelector('.ai-strategy-container');
            container.innerHTML = `
                <h6 class="text-celestial mb-3">Khuyến Nghị Chiến Thuật</h6>
                ${strategies.map(strategy => `
                    <div class="strategy-card mb-3">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="text-purple">${strategy.title}</h6>
                            <span class="priority-badge priority-${strategy.priority.toLowerCase()}">
                                ${strategy.priority}
                            </span>
                        </div>
                        <p class="text-light">${strategy.description}</p>
                        <div class="strategy-impact">
                            <small class="text-golden">
                                <i class="fas fa-arrow-up me-1"></i>
                                Tác động: ${strategy.impact}
                            </small>
                        </div>
                    </div>
                `).join('')}
                
                <div class="ai-conclusion mt-4 p-3 bg-dark bg-opacity-25 rounded">
                    <h6 class="text-golden">Kết Luận AI</h6>
                    <p class="text-light mb-0">
                        Bang hội đang trong giai đoạn phát triển tốt. Ưu tiên tuyển dụng thành viên chất lượng 
                        và tăng cường hoạt động kinh tế để chuẩn bị cho các cuộc chiến lớn.
                    </p>
                </div>
            `;

            // Add strategy styles
            if (!document.getElementById('strategy-styles')) {
                const style = document.createElement('style');
                style.id = 'strategy-styles';
                style.textContent = `
                    .strategy-card {
                        background: rgba(79, 172, 254, 0.1);
                        border: 1px solid rgba(79, 172, 254, 0.3);
                        border-radius: 10px;
                        padding: 1rem;
                    }
                    .priority-badge {
                        padding: 0.25rem 0.5rem;
                        border-radius: 12px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    }
                    .priority-cao { background: rgba(220, 53, 69, 0.2); color: #dc3545; }
                    .priority-trung-bình { background: rgba(255, 193, 7, 0.2); color: #ffc107; }
                    .priority-thấp { background: rgba(40, 167, 69, 0.2); color: #28a745; }
                `;
                document.head.appendChild(style);
            }

        } catch (error) {
            const container = modal.querySelector('.ai-strategy-container');
            container.innerHTML = '<p class="text-danger">Không thể tải chiến thuật AI</p>';
        }
    }

    setupGuildAnalytics() {
        // Create guild performance chart
        const analyticsContainer = document.getElementById('guildAnalytics');
        if (analyticsContainer) {
            this.renderGuildAnalytics();
        }
    }

    renderGuildAnalytics() {
        // This would render guild performance charts
        // Implementation depends on specific analytics requirements
    }

    refreshMemberList() {
        // Refresh the member list display
        setTimeout(() => {
            location.reload();
        }, 1000);
    }

    startGuildUpdates() {
        // Update guild information periodically
        this.memberUpdateTimer = setInterval(() => {
            this.updateGuildStats();
        }, 60000); // Update every minute
    }

    updateGuildStats() {
        // Update guild statistics in real-time
        this.updateMemberActivity();
        this.updateGuildResources();
        this.checkWarStatus();
    }

    updateMemberActivity() {
        const memberItems = document.querySelectorAll('.member-item');
        memberItems.forEach(item => {
            // Add activity indicators
            if (Math.random() < 0.3) {
                item.classList.add('member-active');
                setTimeout(() => {
                    item.classList.remove('member-active');
                }, 2000);
            }
        });
    }

    updateGuildResources() {
        const treasuryEl = document.querySelector('[data-guild-treasury]');
        if (treasuryEl) {
            const current = parseInt(treasuryEl.textContent.replace(/[^\d]/g, '')) || 0;
            const increase = Math.floor(Math.random() * 100) + 50;
            window.tuTienApp.animateNumberChange(treasuryEl, current + increase);
        }
    }

    checkWarStatus() {
        // Check for war status updates
        const warCards = document.querySelectorAll('.war-card');
        warCards.forEach(card => {
            // Add pulsing effect for active wars
            if (Math.random() < 0.2) {
                card.style.animation = 'pulse 1s ease-in-out';
                setTimeout(() => {
                    card.style.animation = '';
                }, 1000);
            }
        });
    }

    // Cleanup
    destroy() {
        if (this.memberUpdateTimer) {
            clearInterval(this.memberUpdateTimer);
        }
    }
}

// Global guild functions
// Custom modal functions
function openCreateGuildModal() {
    const modal = document.getElementById('createGuildModal');
    modal.style.display = 'block';
    modal.classList.add('show');
    modal.style.backgroundColor = 'rgba(15, 15, 35, 0.8)';
    document.body.style.overflow = 'hidden';
    
    // Reset form
    const form = document.getElementById('createGuildForm');
    form.reset();
    
    // Add click outside to close
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeCreateGuildModal();
        }
    });
}

function closeCreateGuildModal() {
    const modal = document.getElementById('createGuildModal');
    modal.style.display = 'none';
    modal.classList.remove('show');
    document.body.style.overflow = '';
    
    // Remove any lingering backdrops
    const backdrops = document.querySelectorAll('.modal-backdrop');
    backdrops.forEach(backdrop => backdrop.remove());
    document.body.classList.remove('modal-open');
    document.body.style.paddingRight = '';
}

async function createGuild() {
    if (window.guildManager) {
        await window.guildManager.handleGuildCreation();
    }
}

function declareWarAgainst(guildId, guildName) {
    // Pre-fill war declaration form
    const targetSelect = document.querySelector('select[name="target_guild_id"]');
    if (targetSelect) {
        targetSelect.value = guildId;
    }
    
    // Open war declaration modal
    const modal = new bootstrap.Modal(document.getElementById('declareWarModal'));
    modal.show();
}

function requestJoinGuild(guildId) {
    if (confirm('Bạn có muốn gửi yêu cầu gia nhập bang hội này?')) {
        fetch('/api/request-join-guild', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ guild_id: guildId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.tuTienApp.showNotification('Yêu Cầu Gửi', 'Đã gửi yêu cầu gia nhập bang hội!', 'success');
            } else {
                window.tuTienApp.showNotification('Lỗi', data.error, 'error');
            }
        })
        .catch(error => {
            window.tuTienApp.showNotification('Lỗi', 'Không thể gửi yêu cầu!', 'error');
        });
    }
}

function viewGuildDetails(guildId) {
    // Implementation for viewing guild details
    window.tuTienApp.showNotification('Thông Tin Bang Hội', 'Tính năng xem chi tiết sẽ được phát triển!', 'info');
}

function viewWarDetails(warId) {
    // Implementation for viewing war details
    window.tuTienApp.showNotification('Chi Tiết Chiến Tranh', 'Tính năng xem chi tiết chiến tranh sẽ được phát triển!', 'info');
}

function sendReinforcments(warId) {
    // Implementation for sending reinforcements
    window.tuTienApp.showNotification('Viện Trợ', 'Tính năng viện trợ chiến tranh sẽ được phát triển!', 'info');
}

// Initialize guild manager on page load
document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('guild-page') || window.location.pathname.includes('guild')) {
        window.guildManager = new GuildManager();
        console.log('Guild Manager initialized successfully!');
    }
});
