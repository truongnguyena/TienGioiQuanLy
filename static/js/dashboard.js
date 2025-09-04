// Dashboard specific JavaScript functionality
class Dashboard {
    constructor() {
        this.cultivationTimer = null;
        this.aiAdviceTimer = null;
        this.resourceUpdateTimer = null;
        this.init();
    }

    init() {
        this.setupCultivationSystem();
        this.setupAIInteractions();
        this.setupResourceManagement();
        this.setupGuildQuickActions();
        this.startDashboardUpdates();
    }

    setupCultivationSystem() {
        // Auto-cultivation toggle
        const autoCultivateToggle = document.getElementById('autoCultivate');
        if (autoCultivateToggle) {
            autoCultivateToggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.startAutoCultivation();
                } else {
                    this.stopAutoCultivation();
                }
            });
        }

        // Cultivation progress animation
        this.animateCultivationProgress();
    }

    async cultivate() {
        const cultivateBtn = document.querySelector('[onclick="cultivate()"]');
        if (!cultivateBtn) return;

        const originalText = cultivateBtn.innerHTML;
        showLoading(cultivateBtn);

        try {
            const response = await fetch('/api/cultivate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                // Update spiritual power display
                this.updateSpiritualPower(data.new_total);
                
                // Show cultivation effect
                this.showCultivationEffect(data.power_gained);
                
                // Update cultivation level if changed
                if (data.cultivation_level) {
                    this.updateCultivationLevel(data.cultivation_level);
                }

                // Show success notification
                window.tuTienApp.showNotification(
                    'Tu Luyện Thành Công!', 
                    `Tăng ${data.power_gained} điểm linh lực`, 
                    'cultivation'
                );

                // Check for breakthrough
                this.checkBreakthrough(data);
            } else {
                throw new Error(data.error || 'Cultivation failed');
            }
        } catch (error) {
            console.error('Cultivation error:', error);
            window.tuTienApp.showNotification('Lỗi Tu Luyện', error.message, 'error');
        } finally {
            hideLoading(cultivateBtn, originalText);
        }
    }

    updateSpiritualPower(newPower) {
        const powerElement = document.querySelector('[data-spiritual-power]');
        if (powerElement) {
            window.tuTienApp.animateNumberChange(powerElement, newPower);
        }

        // Update progress bar
        const progressBar = document.querySelector('.progress-bar-golden');
        if (progressBar) {
            const percentage = (newPower % 1000) / 10;
            progressBar.style.width = `${percentage}%`;
        }
    }

    updateCultivationLevel(newLevel) {
        const levelElements = document.querySelectorAll('[data-cultivation-level]');
        levelElements.forEach(element => {
            element.textContent = newLevel;
        });
    }

    showCultivationEffect(powerGained) {
        // Create floating power gain effect
        const effect = document.createElement('div');
        effect.className = 'cultivation-effect';
        effect.textContent = `+${powerGained}`;
        effect.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #ffd700;
            font-size: 2rem;
            font-weight: bold;
            pointer-events: none;
            z-index: 9999;
            animation: cultivationGain 2s ease-out forwards;
        `;

        if (!document.getElementById('cultivation-effects-style')) {
            const style = document.createElement('style');
            style.id = 'cultivation-effects-style';
            style.textContent = `
                @keyframes cultivationGain {
                    0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
                    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
                    100% { opacity: 0; transform: translate(-50%, -100px) scale(0.8); }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), 2000);

        // Add cultivation aura effect
        this.addCultivationAura();
    }

    addCultivationAura() {
        const avatar = document.querySelector('.avatar-container');
        if (avatar) {
            avatar.classList.add('cultivation-active');
            setTimeout(() => {
                avatar.classList.remove('cultivation-active');
            }, 3000);
        }
    }

    checkBreakthrough(data) {
        if (data.breakthrough) {
            // Major breakthrough effect
            this.showBreakthroughEffect(data.new_stage);
        }
    }

    showBreakthroughEffect(newStage) {
        // Full screen breakthrough effect
        const overlay = document.createElement('div');
        overlay.className = 'breakthrough-overlay';
        overlay.innerHTML = `
            <div class="breakthrough-content">
                <h1 class="breakthrough-title">突破成功!</h1>
                <h2 class="breakthrough-stage">${newStage}</h2>
                <div class="breakthrough-particles"></div>
            </div>
        `;
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(255, 215, 0, 0.3), rgba(0, 0, 0, 0.8));
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: breakthroughFade 4s ease-out forwards;
        `;

        document.body.appendChild(overlay);

        // Auto remove after animation
        setTimeout(() => overlay.remove(), 4000);

        // Play breakthrough sound if available
        this.playBreakthroughSound();
    }

    playBreakthroughSound() {
        // Create audio context for breakthrough sound
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            const audioContext = new (AudioContext || webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(880, audioContext.currentTime + 0.5);
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 1);
        }
    }

    startAutoCultivation() {
        this.cultivationTimer = setInterval(() => {
            this.cultivate();
        }, 60000); // Auto cultivate every minute

        window.tuTienApp.showNotification('Tự Động Tu Luyện', 'Đã bật chế độ tự động tu luyện', 'info');
    }

    stopAutoCultivation() {
        if (this.cultivationTimer) {
            clearInterval(this.cultivationTimer);
            this.cultivationTimer = null;
        }
        window.tuTienApp.showNotification('Tự Động Tu Luyện', 'Đã tắt chế độ tự động tu luyện', 'info');
    }

    animateCultivationProgress() {
        const progressBar = document.querySelector('.progress-bar-golden');
        if (progressBar) {
            // Add breathing animation to progress bar
            setInterval(() => {
                progressBar.style.filter = 'brightness(1.2)';
                setTimeout(() => {
                    progressBar.style.filter = 'brightness(1)';
                }, 1000);
            }, 2000);
        }
    }

    setupAIInteractions() {
        // AI fortune refresh
        const refreshFortuneBtn = document.getElementById('refreshFortune');
        if (refreshFortuneBtn) {
            refreshFortuneBtn.addEventListener('click', () => {
                this.refreshAIFortune();
            });
        }

        // AI advice interaction
        this.setupAIAdviceInteraction();
    }

    async refreshAIFortune() {
        const fortuneContainer = document.querySelector('.fortune-text');
        if (!fortuneContainer) return;

        // Show loading
        const originalFortune = fortuneContainer.innerHTML;
        fortuneContainer.innerHTML = '<div class="loading-spinner"></div><p class="text-light mt-2">AI đang tính toán vận mệnh...</p>';

        try {
            // Simulate AI fortune generation
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            const fortunes = [
                "Hôm nay là ngày tốt lành cho việc đột phá cảnh giới cao hơn!",
                "Nên tránh tu luyện công pháp mạnh trong 3 ngày tới để tránh tẩu hỏa nhập ma.",
                "Có cơ hội gặp được cao nhân chỉ điểm đạo pháp trong tuần này.",
                "Thiên kiếp sắp tới, hãy chuẩn bị tâm lý và tài nguyên cẩn thận.",
                "Vận mệnh thuận lợi cho việc luyện đan dược và chế tạo pháp bảo.",
                "Thích hợp khám phá bí cảnh để tìm kiếm cơ duyên và báu vật.",
                "Nên tập trung vào tu luyện thần thức và tâm pháp.",
                "Có thể gặp phải tiểu nhân, cần cảnh giác trong giao dịch."
            ];

            const newFortune = fortunes[Math.floor(Math.random() * fortunes.length)];
            fortuneContainer.innerHTML = `
                <i class="fas fa-quote-left text-golden opacity-50"></i>
                <p class="text-light mt-2">${newFortune}</p>
                <i class="fas fa-quote-right text-golden opacity-50 float-end"></i>
            `;

            window.tuTienApp.showNotification('AI Dự Đoán', 'Đã cập nhật vận mệnh mới!', 'info');
        } catch (error) {
            fortuneContainer.innerHTML = originalFortune;
            window.tuTienApp.showNotification('Lỗi', 'Không thể cập nhật vận mệnh!', 'error');
        }
    }

    setupAIAdviceInteraction() {
        // Create AI chat interface
        const aiChatBtn = document.getElementById('aiChatBtn');
        if (aiChatBtn) {
            aiChatBtn.addEventListener('click', () => {
                this.openAIChat();
            });
        }
    }

    openAIChat() {
        // Create AI chat modal
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content mystical-modal">
                    <div class="modal-header border-bottom border-secondary">
                        <h5 class="modal-title text-golden">
                            <i class="fas fa-robot me-2"></i>AI Tu Tiên Cố Vấn
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="ai-chat-container" style="height: 400px; overflow-y: auto; padding: 1rem; background: rgba(15, 15, 35, 0.3); border-radius: 10px;">
                            <div class="ai-message">
                                <strong class="text-golden">AI Cố Vấn:</strong>
                                <p class="text-light">Xin chào, ta là AI cố vấn tu tiên. Hãy hỏi ta về bất kỳ điều gì liên quan đến tu luyện!</p>
                            </div>
                        </div>
                        <div class="ai-chat-input mt-3">
                            <div class="input-group">
                                <input type="text" class="form-control mystical-input" id="aiChatInput" placeholder="Hỏi AI về tu luyện...">
                                <button class="btn btn-golden mystical-btn" onclick="dashboard.sendAIMessage()">
                                    <i class="fas fa-paper-plane"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();

        // Clean up on close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    async sendAIMessage() {
        const input = document.getElementById('aiChatInput');
        const container = document.querySelector('.ai-chat-container');
        
        if (!input || !container || !input.value.trim()) return;

        const message = input.value.trim();
        input.value = '';

        // Add user message
        const userMessage = document.createElement('div');
        userMessage.className = 'user-message mb-3';
        userMessage.innerHTML = `
            <strong class="text-celestial">Bạn:</strong>
            <p class="text-light">${message}</p>
        `;
        container.appendChild(userMessage);

        // Add AI thinking indicator
        const thinkingMessage = document.createElement('div');
        thinkingMessage.className = 'ai-thinking mb-3';
        thinkingMessage.innerHTML = `
            <strong class="text-golden">AI Cố Vấn:</strong>
            <p class="text-light"><i class="fas fa-circle-notch fa-spin me-2"></i>Đang suy nghĩ...</p>
        `;
        container.appendChild(thinkingMessage);
        container.scrollTop = container.scrollHeight;

        try {
            // Simulate AI response
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            const responses = this.generateAIResponse(message);
            thinkingMessage.remove();

            const aiMessage = document.createElement('div');
            aiMessage.className = 'ai-message mb-3';
            aiMessage.innerHTML = `
                <strong class="text-golden">AI Cố Vấn:</strong>
                <p class="text-light">${responses}</p>
            `;
            container.appendChild(aiMessage);
            container.scrollTop = container.scrollHeight;

        } catch (error) {
            thinkingMessage.remove();
            const errorMessage = document.createElement('div');
            errorMessage.className = 'ai-message mb-3';
            errorMessage.innerHTML = `
                <strong class="text-golden">AI Cố Vấn:</strong>
                <p class="text-danger">Xin lỗi, ta đang gặp vấn đề. Hãy thử lại sau.</p>
            `;
            container.appendChild(errorMessage);
        }
    }

    generateAIResponse(message) {
        const keywords = message.toLowerCase();
        
        if (keywords.includes('tu luyện') || keywords.includes('cultivation')) {
            return "Để tu luyện hiệu quả, nên duy trì thói quen tu luyện hàng ngày, sử dụng đan dược hỗ trợ và tìm kiếm môi trường có linh khí dồi dào. Nhớ không được vội vàng đột phá khi chưa đủ cơ sở.";
        } else if (keywords.includes('đột phá') || keywords.includes('breakthrough')) {
            return "Đột phá cảnh giới cần chuẩn bị kỹ lưỡng: tích lũy đủ linh lực, có đan dược hỗ trợ, chọn thời điểm thích hợp và tâm trạng ổn định. Không nên ép buộc đột phá khi chưa sẵn sàng.";
        } else if (keywords.includes('bang hội') || keywords.includes('guild')) {
            return "Tham gia bang hội mạnh sẽ có nhiều lợi ích: chia sẻ tài nguyên, học hỏi kinh nghiệm, tham gia đạo lữ nhóm và được bảo vệ. Hãy chọn bang hội phù hợp với phong cách tu luyện của bạn.";
        } else if (keywords.includes('đạo lữ') || keywords.includes('expedition')) {
            return "Đạo lữ là cách tốt để thu thập tài nguyên và tăng kinh nghiệm. Chuẩn bị đầy đủ vật phẩm, tìm hiểu về điểm đến và hợp tác tốt với đồng đội để đảm bảo an toàn.";
        } else if (keywords.includes('pháp bảo') || keywords.includes('tài nguyên')) {
            return "Quản lý tài nguyên thông minh: ưu tiên nâng cấp pháp bảo chính, đầu tư vào đan dược chất lượng, và luôn dự trữ một phần cho trường hợp khẩn cấp.";
        } else {
            return "Ta hiểu bạn quan tâm đến con đường tu tiên. Hãy hỏi cụ thể hơn về tu luyện, đột phá, bang hội, đạo lữ hoặc quản lý tài nguyên để ta có thể tư vấn tốt hơn.";
        }
    }

    setupResourceManagement() {
        // Resource auto-collection
        this.startResourceUpdates();
        
        // Quick resource actions
        this.setupQuickResourceActions();
    }

    startResourceUpdates() {
        this.resourceUpdateTimer = setInterval(() => {
            this.updateResources();
        }, 60000); // Update every minute
    }

    updateResources() {
        // Simulate resource generation
        const spiritualStones = document.querySelector('[data-spiritual-stones]');
        const pills = document.querySelector('[data-pills]');
        
        if (spiritualStones) {
            const current = parseInt(spiritualStones.textContent) || 0;
            const gained = Math.floor(Math.random() * 10) + 5;
            window.tuTienApp.animateNumberChange(spiritualStones, current + gained);
        }

        if (Math.random() < 0.1 && pills) { // 10% chance to gain pills
            const current = parseInt(pills.textContent) || 0;
            window.tuTienApp.animateNumberChange(pills, current + 1);
            window.tuTienApp.showNotification('Tài Nguyên', 'Tìm thấy đan dược!', 'success');
        }
    }

    setupQuickResourceActions() {
        // Quick use pills button
        const quickUsePillBtn = document.getElementById('quickUsePill');
        if (quickUsePillBtn) {
            quickUsePillBtn.addEventListener('click', () => {
                this.quickUsePill();
            });
        }

        // Resource exchange
        const exchangeBtn = document.getElementById('resourceExchange');
        if (exchangeBtn) {
            exchangeBtn.addEventListener('click', () => {
                this.openResourceExchange();
            });
        }
    }

    quickUsePill() {
        const pillsCount = document.querySelector('[data-pills]');
        const currentPills = parseInt(pillsCount?.textContent) || 0;
        
        if (currentPills > 0) {
            // Use pill and gain spiritual power
            window.tuTienApp.animateNumberChange(pillsCount, currentPills - 1);
            
            const powerGain = Math.floor(Math.random() * 100) + 50;
            const currentPower = parseInt(document.querySelector('[data-spiritual-power]')?.textContent?.replace(/[^\d]/g, '')) || 0;
            this.updateSpiritualPower(currentPower + powerGain);
            
            window.tuTienApp.showNotification('Sử Dụng Đan Dược', `Tăng ${powerGain} linh lực!`, 'success');
        } else {
            window.tuTienApp.showNotification('Không Đủ Đan Dược', 'Cần có ít nhất 1 đan dược để sử dụng!', 'warning');
        }
    }

    openResourceExchange() {
        // Resource exchange interface would be implemented here
        window.tuTienApp.showNotification('Sàn Giao Dịch', 'Tính năng sàn giao dịch sẽ được phát triển!', 'info');
    }

    setupGuildQuickActions() {
        // Quick guild war declaration
        const quickWarBtn = document.getElementById('quickWar');
        if (quickWarBtn) {
            quickWarBtn.addEventListener('click', () => {
                this.openQuickWarInterface();
            });
        }

        // Guild contribution
        const contributeBtn = document.getElementById('guildContribute');
        if (contributeBtn) {
            contributeBtn.addEventListener('click', () => {
                this.openGuildContribution();
            });
        }
    }

    openQuickWarInterface() {
        // Quick war declaration interface
        window.tuTienApp.showNotification('Tuyên Chiến Nhanh', 'Tính năng tuyên chiến nhanh sẽ được phát triển!', 'info');
    }

    openGuildContribution() {
        // Guild contribution interface
        window.tuTienApp.showNotification('Đóng Góp Bang Hội', 'Tính năng đóng góp bang hội sẽ được phát triển!', 'info');
    }

    startDashboardUpdates() {
        // Real-time dashboard updates
        setInterval(() => {
            this.updateDashboardStats();
        }, 30000); // Update every 30 seconds
    }

    updateDashboardStats() {
        // Update various dashboard statistics
        this.updateOnlineCount();
        this.updateGuildActivity();
        this.updateExpeditionStatus();
    }

    updateOnlineCount() {
        const onlineCountEl = document.querySelector('[data-online-count]');
        if (onlineCountEl) {
            const count = Math.floor(Math.random() * 50) + 20;
            onlineCountEl.textContent = count;
        }
    }

    updateGuildActivity() {
        // Update guild activity indicators
        const guildActivityEl = document.querySelector('[data-guild-activity]');
        if (guildActivityEl) {
            const activities = ['Đang tu luyện', 'Tham gia đạo lữ', 'Giao dịch', 'Offline'];
            const activity = activities[Math.floor(Math.random() * activities.length)];
            guildActivityEl.textContent = activity;
        }
    }

    updateExpeditionStatus() {
        // Update expedition status
        const expeditionStatusEl = document.querySelector('[data-expedition-status]');
        if (expeditionStatusEl) {
            const statuses = ['Sẵn sàng tham gia', 'Đang trong đạo lữ', 'Chờ phần thưởng'];
            const status = statuses[Math.floor(Math.random() * statuses.length)];
            expeditionStatusEl.textContent = status;
        }
    }

    // Cleanup when leaving dashboard
    destroy() {
        if (this.cultivationTimer) {
            clearInterval(this.cultivationTimer);
        }
        if (this.aiAdviceTimer) {
            clearInterval(this.aiAdviceTimer);
        }
        if (this.resourceUpdateTimer) {
            clearInterval(this.resourceUpdateTimer);
        }
    }
}

// Global functions for dashboard
async function cultivate() {
    if (window.dashboard) {
        await window.dashboard.cultivate();
    }
}

async function createGuild() {
    const form = document.getElementById('createGuildForm');
    if (!form) return;

    const formData = new FormData(form);
    const guildData = {
        name: formData.get('name'),
        description: formData.get('description')
    };

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
            window.tuTienApp.showNotification('Thành Công', data.message, 'success');
            setTimeout(() => {
                location.reload();
            }, 1500);
        } else {
            window.tuTienApp.showNotification('Lỗi', data.error, 'error');
        }
    } catch (error) {
        window.tuTienApp.showNotification('Lỗi', 'Không thể tạo bang hội!', 'error');
    }
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('dashboard-page') || window.location.pathname.includes('dashboard')) {
        window.dashboard = new Dashboard();
        console.log('Dashboard initialized successfully!');
    }
});
