// Global expedition functions
function openCreateExpeditionModal() {
    const modal = document.getElementById('createExpeditionModal');
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('show');
        modal.style.backgroundColor = 'rgba(15, 15, 35, 0.8)';
        document.body.style.overflow = 'hidden';
        
        // Reset form
        const form = document.getElementById('createExpeditionForm');
        if (form) form.reset();
        
        // Add click outside to close
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeCreateExpeditionModal();
            }
        });
    }
}

function closeCreateExpeditionModal() {
    const modal = document.getElementById('createExpeditionModal');
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

async function joinExpedition(expeditionId) {
    if (!confirm('Bạn có chắc muốn tham gia đạo lữ này?')) return;
    
    try {
        const response = await fetch('/api/join-expedition', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expedition_id: expeditionId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Đã tham gia đạo lữ thành công!');
            location.reload();
        } else {
            alert('Lỗi: ' + (data.error || 'Không thể tham gia'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Có lỗi xảy ra!');
    }
}

// Expeditions JavaScript functionality
class ExpeditionManager {
    constructor() {
        this.activeExpeditions = [];
        this.availableExpeditions = [];
        this.expeditionTimer = null;
        this.routeGenerator = null;
        this.init();
    }

    init() {
        this.setupExpeditionActions();
        this.setupAIRouteGenerator();
        this.setupExpeditionTracking();
        this.setupResourceManagement();
        this.startExpeditionUpdates();
    }

    setupExpeditionActions() {
        // Expedition creation form
        const createExpeditionForm = document.getElementById('createExpeditionForm');
        if (createExpeditionForm) {
            createExpeditionForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleExpeditionCreation();
            });
        }

        // Join expedition buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('[onclick*="joinExpedition"]')) {
                e.preventDefault();
                const expeditionId = this.extractExpeditionId(e.target.getAttribute('onclick'));
                this.handleJoinExpedition(expeditionId);
            }
        });

        // Quick expedition search
        const expeditionSearch = document.getElementById('expeditionSearch');
        if (expeditionSearch) {
            expeditionSearch.addEventListener('input', (e) => {
                this.filterExpeditions(e.target.value);
            });
        }
    }

    async handleExpeditionCreation() {
        const form = document.getElementById('createExpeditionForm');
        const formData = new FormData(form);
        
        const expeditionData = {
            name: formData.get('name'),
            destination: formData.get('destination'),
            description: formData.get('description'),
            difficulty_level: parseInt(formData.get('difficulty_level')),
            max_participants: parseInt(formData.get('max_participants')),
            duration_hours: parseInt(formData.get('duration_hours')),
            min_cultivation: formData.get('min_cultivation'),
            required_items: formData.get('required_items'),
            potential_rewards: formData.get('potential_rewards')
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        showLoading(submitBtn);

        try {
            const response = await fetch('/api/create-expedition', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(expeditionData)
            });

            const data = await response.json();

            if (data.success) {
                this.showExpeditionCreationEffect();
                window.tuTienApp.showNotification(
                    'Đạo Lữ Thành Lập!', 
                    `Đã tạo đạo lữ "${expeditionData.name}" thành công`, 
                    'success'
                );
                
                // Close modal and refresh
                const modal = bootstrap.Modal.getInstance(document.getElementById('createExpeditionModal'));
                modal.hide();
                
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                throw new Error(data.error || 'Không thể tạo đạo lữ');
            }
        } catch (error) {
            console.error('Expedition creation error:', error);
            window.tuTienApp.showNotification('Lỗi Tạo Đạo Lữ', error.message, 'error');
        } finally {
            hideLoading(submitBtn, originalText);
        }
    }

    showExpeditionCreationEffect() {
        // Create expedition creation effect
        const effect = document.createElement('div');
        effect.className = 'expedition-creation-effect';
        effect.innerHTML = `
            <div class="expedition-effect-content">
                <h1 class="expedition-title">🗺️ ĐẠO LỮ KHAI KHỞI! 🗺️</h1>
                <div class="expedition-sparkles"></div>
            </div>
        `;
        effect.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, rgba(79, 172, 254, 0.3), rgba(0, 0, 0, 0.8));
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: expeditionFade 2.5s ease-out forwards;
        `;

        if (!document.getElementById('expedition-effects-style')) {
            const style = document.createElement('style');
            style.id = 'expedition-effects-style';
            style.textContent = `
                @keyframes expeditionFade {
                    0% { opacity: 0; }
                    20% { opacity: 1; }
                    80% { opacity: 1; }
                    100% { opacity: 0; }
                }
                .expedition-title {
                    color: #4facfe;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
                    font-size: 2.5rem;
                    animation: glow 1s ease-in-out infinite alternate;
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(effect);
        setTimeout(() => effect.remove(), 2500);
    }

    extractExpeditionId(onclickAttr) {
        const match = onclickAttr.match(/joinExpedition\((\d+)\)/);
        return match ? parseInt(match[1]) : null;
    }

    async handleJoinExpedition(expeditionId) {
        if (!expeditionId) return;

        try {
            const response = await fetch(`/api/join-expedition/${expeditionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showJoinExpeditionEffect();
                window.tuTienApp.showNotification(
                    'Tham Gia Đạo Lữ!', 
                    data.message, 
                    'success'
                );
                
                // Update UI
                this.updateExpeditionParticipants(expeditionId);
            } else {
                throw new Error(data.error || 'Không thể tham gia đạo lữ');
            }
        } catch (error) {
            console.error('Join expedition error:', error);
            window.tuTienApp.showNotification('Lỗi Tham Gia', error.message, 'error');
        }
    }

    showJoinExpeditionEffect() {
        // Create join expedition effect with particles
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.className = 'expedition-particle';
            particle.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: #4facfe;
                border-radius: 50%;
                pointer-events: none;
                z-index: 9998;
                left: ${Math.random() * window.innerWidth}px;
                top: ${Math.random() * window.innerHeight}px;
                animation: expeditionParticle 2s ease-out forwards;
            `;

            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 2000);
        }

        if (!document.getElementById('expedition-particle-style')) {
            const style = document.createElement('style');
            style.id = 'expedition-particle-style';
            style.textContent = `
                @keyframes expeditionParticle {
                    0% { 
                        opacity: 1; 
                        transform: scale(1) translateY(0); 
                    }
                    100% { 
                        opacity: 0; 
                        transform: scale(0.5) translateY(-100px); 
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    updateExpeditionParticipants(expeditionId) {
        // Update the participants display for the expedition
        const expeditionCard = document.querySelector(`[data-expedition-id="${expeditionId}"]`);
        if (expeditionCard) {
            const participantsCount = expeditionCard.querySelector('.participants-badge');
            if (participantsCount) {
                const current = participantsCount.textContent.match(/(\d+)\/(\d+)/);
                if (current) {
                    const newCount = parseInt(current[1]) + 1;
                    const max = current[2];
                    participantsCount.innerHTML = `<i class="fas fa-users me-1"></i>${newCount}/${max}`;
                }
            }
        }
    }

    filterExpeditions(searchTerm) {
        const expeditionCards = document.querySelectorAll('.expedition-card');
        searchTerm = searchTerm.toLowerCase();

        expeditionCards.forEach(card => {
            const title = card.querySelector('h5, h6').textContent.toLowerCase();
            const description = card.querySelector('p').textContent.toLowerCase();
            const destination = card.querySelector('[data-destination]')?.textContent.toLowerCase() || '';

            if (title.includes(searchTerm) || description.includes(searchTerm) || destination.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    setupAIRouteGenerator() {
        // AI route generation button
        const generateRouteBtn = document.getElementById('generateRouteBtn');
        if (generateRouteBtn) {
            generateRouteBtn.addEventListener('click', () => {
                this.generateAIRoute();
            });
        }

        // Route difficulty selector
        const difficultySlider = document.querySelector('input[name="difficulty_level"]');
        if (difficultySlider) {
            difficultySlider.addEventListener('input', (e) => {
                this.updateRouteSuggestions(parseInt(e.target.value));
            });
        }
    }

    async generateAIRoute() {
        const difficultyLevel = document.querySelector('input[name="difficulty_level"]')?.value || 3;
        const destination = document.querySelector('select[name="destination"]')?.value || 'Rừng Tre Xanh';
        
        const routeContainer = document.getElementById('generated-route');
        const routeInfo = routeContainer.querySelector('.route-info');
        
        routeContainer.style.display = 'block';
        routeInfo.innerHTML = '<div class="loading-spinner"></div><p class="text-light mt-2">AI đang tạo lộ trình...</p>';

        try {
            // Simulate AI route generation
            await new Promise(resolve => setTimeout(resolve, 2000));

            const route = this.generateRouteData(parseInt(difficultyLevel), destination);
            
            routeInfo.innerHTML = `
                <h6 class="text-golden mb-3">
                    <i class="fas fa-route me-2"></i>Lộ Trình AI Tạo
                </h6>
                
                <div class="route-waypoints mb-3">
                    <h6 class="text-celestial">Các Điểm Dừng:</h6>
                    <div class="waypoint-list">
                        ${route.waypoints.map(waypoint => `
                            <span class="route-waypoint">${waypoint}</span>
                        `).join('')}
                    </div>
                </div>
                
                <div class="route-details mb-3">
                    <div class="row">
                        <div class="col-6">
                            <small class="text-light">Thời Gian Dự Kiến:</small>
                            <div class="text-celestial">${route.estimated_time}</div>
                        </div>
                        <div class="col-6">
                            <small class="text-light">Độ Nguy Hiểm:</small>
                            <div class="text-purple">Cấp ${difficultyLevel}</div>
                        </div>
                    </div>
                </div>
                
                <div class="route-supplies mb-3">
                    <h6 class="text-celestial">Vật Phẩm Khuyến Nghị:</h6>
                    <div class="supply-list">
                        ${route.recommended_supplies.map(supply => `
                            <span class="supply-item">${supply}</span>
                        `).join('')}
                    </div>
                </div>
                
                <div class="route-events">
                    <h6 class="text-golden">Sự Kiện Đặc Biệt:</h6>
                    <ul class="list-unstyled">
                        ${route.special_events.map(event => `
                            <li class="text-light">
                                <i class="fas fa-star text-warning me-2"></i>
                                ${event}
                            </li>
                        `).join('')}
                    </ul>
                </div>
                
                <div class="route-actions mt-3">
                    <button class="btn btn-sm btn-purple mystical-btn me-2" onclick="expeditionManager.applyGeneratedRoute()">
                        <i class="fas fa-check me-1"></i>Áp Dụng Lộ Trình
                    </button>
                    <button class="btn btn-sm btn-outline-celestial mystical-btn" onclick="expeditionManager.generateAIRoute()">
                        <i class="fas fa-sync me-1"></i>Tạo Lại
                    </button>
                </div>
            `;

            // Add styles if not exists
            if (!document.getElementById('route-styles')) {
                const style = document.createElement('style');
                style.id = 'route-styles';
                style.textContent = `
                    .route-waypoint {
                        background: rgba(79, 172, 254, 0.2);
                        color: var(--celestial);
                        padding: 0.25rem 0.5rem;
                        border-radius: 8px;
                        margin: 0.25rem;
                        display: inline-block;
                        font-size: 0.85rem;
                    }
                    .supply-item {
                        background: rgba(142, 45, 226, 0.2);
                        color: var(--purple);
                        padding: 0.25rem 0.5rem;
                        border-radius: 8px;
                        margin: 0.25rem;
                        display: inline-block;
                        font-size: 0.85rem;
                    }
                    .waypoint-list, .supply-list {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.25rem;
                    }
                `;
                document.head.appendChild(style);
            }

            window.tuTienApp.showNotification('AI Lộ Trình', 'Đã tạo lộ trình thông minh!', 'success');

        } catch (error) {
            routeInfo.innerHTML = '<p class="text-danger">Không thể tạo lộ trình. Vui lòng thử lại.</p>';
            window.tuTienApp.showNotification('Lỗi AI', 'Không thể tạo lộ trình!', 'error');
        }
    }

    generateRouteData(difficulty, destination) {
        const routes = {
            1: {
                waypoints: ["Làng Khởi Đầu", "Rừng Tre Xanh", "Suối Linh Tuyền", "Đồi Hoa Lan"],
                supplies: ["Đan dược cơ bản", "Nước uống", "Bùa may mắn"],
                events: ["Gặp thú cưng hiền lành", "Tìm thấy linh thảo phổ biến"]
            },
            2: {
                waypoints: ["Trạm Dừng An Toàn", "Thung Lũng Sương Mù", "Hang Dơi Máu", "Đỉnh Núi Kiếm"],
                supplies: ["Đan dược hồi phục", "Pháp bảo phòng thủ", "Bùa trừ tà"],
                events: ["15% cơ hội gặp Linh Thú cấp 2", "Có thể tìm thấy khoáng chất quý"]
            },
            3: {
                waypoints: ["Cửa Ải Nguy Hiểm", "Sa Mạc Cát Vàng", "Đền Cổ Bỏ Hoang", "Hồ Nước Độc"],
                supplies: ["Đan dược cao cấp", "Pháp bảo tấn công", "Linh thạch dự phòng"],
                events: ["25% cơ hội gặp Boss mini", "Khả năng tìm được Thiên Tài Địa Bảo"]
            },
            4: {
                waypoints: ["Ranh Giới Tử Thần", "Rừng Quỷ Dữ", "Thành Phố Ma", "Cổng Địa Ngục"],
                supplies: ["Đan dược quý hiếm", "Pháp bảo thần bí", "Bùa hộ mạng"],
                events: ["40% cơ hội gặp Ác Quỷ mạnh", "Có thể gặp được cao nhân ẩn dật"]
            },
            5: {
                waypoints: ["Cửa Thiên Giới", "Thiên Đình", "Cung Điện Rồng", "Vực Sâu Vô Đáy"],
                supplies: ["Tiên đan", "Thần khí", "Hộ thân phù"],
                events: ["50% cơ hội gặp Thần Long", "Cơ hội đột phá cảnh giới cao"]
            }
        };

        const routeData = routes[difficulty] || routes[3];
        
        return {
            waypoints: routeData.waypoints,
            estimated_time: `${difficulty * 6}-${difficulty * 8} giờ`,
            recommended_supplies: routeData.supplies,
            special_events: routeData.events
        };
    }

    applyGeneratedRoute() {
        // Apply the generated route to the form
        const routeData = this.getGeneratedRouteData();
        
        // Update form fields
        const suppliesField = document.querySelector('input[name="required_items"]');
        if (suppliesField && routeData.supplies) {
            suppliesField.value = routeData.supplies.join(', ');
        }

        const rewardsField = document.querySelector('textarea[name="potential_rewards"]');
        if (rewardsField && routeData.events) {
            rewardsField.value = routeData.events.join(', ');
        }

        window.tuTienApp.showNotification('Lộ Trình', 'Đã áp dụng lộ trình AI vào đạo lữ!', 'success');
    }

    getGeneratedRouteData() {
        const routeInfo = document.querySelector('.route-info');
        if (!routeInfo) return {};

        const supplies = Array.from(routeInfo.querySelectorAll('.supply-item')).map(item => item.textContent);
        const events = Array.from(routeInfo.querySelectorAll('.route-events li')).map(item => item.textContent.trim());

        return { supplies, events };
    }

    updateRouteSuggestions(difficulty) {
        const destinationSelect = document.querySelector('select[name="destination"]');
        if (!destinationSelect) return;

        // Update destination options based on difficulty
        const destinations = {
            1: ["Rừng Tre Xanh", "Suối Linh Tuyền", "Đồi Hoa Lan"],
            2: ["Thung Lũng Sương Mù", "Hang Dơi Máu", "Đỉnh Núi Kiếm"],
            3: ["Sa Mạc Cát Vàng", "Đền Cổ Bỏ Hoang", "Hồ Nước Độc"],
            4: ["Rừng Quỷ Dữ", "Thành Phố Ma", "Cổng Địa Ngục"],
            5: ["Thiên Đình", "Cung Điện Rồng", "Vực Sâu Vô Đáy"]
        };

        const currentValue = destinationSelect.value;
        const suggestedDestinations = destinations[difficulty] || destinations[3];
        
        // Update options
        destinationSelect.innerHTML = suggestedDestinations.map(dest => 
            `<option value="${dest}" ${dest === currentValue ? 'selected' : ''}>${dest}</option>`
        ).join('');
    }

    setupExpeditionTracking() {
        // Real-time expedition progress tracking
        this.setupProgressTracking();
        
        // Expedition status updates
        this.setupStatusUpdates();
        
        // Participant activity monitoring
        this.setupParticipantTracking();
    }

    setupProgressTracking() {
        const progressBars = document.querySelectorAll('.expedition-progress');
        progressBars.forEach(bar => {
            this.animateProgress(bar);
        });
    }

    animateProgress(progressBar) {
        let progress = 0;
        const targetProgress = Math.random() * 80 + 10; // 10-90%
        
        const interval = setInterval(() => {
            progress += Math.random() * 2;
            if (progress >= targetProgress) {
                progress = targetProgress;
                clearInterval(interval);
            }
            
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${Math.floor(progress)}%`;
        }, 500);
    }

    setupStatusUpdates() {
        // Simulate status updates for active expeditions
        setInterval(() => {
            this.updateExpeditionStatuses();
        }, 30000); // Update every 30 seconds
    }

    updateExpeditionStatuses() {
        const activeExpeditionItems = document.querySelectorAll('.active-expedition-item');
        
        activeExpeditionItems.forEach(item => {
            if (Math.random() < 0.3) { // 30% chance of update
                const statusIndicator = item.querySelector('.expedition-status');
                if (statusIndicator) {
                    this.flashStatusUpdate(statusIndicator);
                }
            }
        });
    }

    flashStatusUpdate(element) {
        element.style.backgroundColor = 'rgba(79, 172, 254, 0.3)';
        element.style.transition = 'background-color 0.5s ease';
        
        setTimeout(() => {
            element.style.backgroundColor = '';
        }, 1000);
    }

    setupParticipantTracking() {
        // Track participant activity
        const participantItems = document.querySelectorAll('.participant-item');
        participantItems.forEach(item => {
            this.addParticipantIndicators(item);
        });
    }

    addParticipantIndicators(participantItem) {
        // Add activity indicator
        const indicator = document.createElement('div');
        indicator.className = 'participant-activity';
        indicator.style.cssText = `
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: ${Math.random() > 0.5 ? '#28a745' : '#6c757d'};
            display: inline-block;
            margin-left: 0.5rem;
        `;
        
        participantItem.appendChild(indicator);
    }

    setupResourceManagement() {
        // Expedition cost calculator
        this.setupCostCalculator();
        
        // Resource requirement checker
        this.setupRequirementChecker();
        
        // Reward distribution system
        this.setupRewardSystem();
    }

    setupCostCalculator() {
        const difficultySlider = document.querySelector('input[name="difficulty_level"]');
        const durationInput = document.querySelector('input[name="duration_hours"]');
        const participantsInput = document.querySelector('input[name="max_participants"]');
        
        if (difficultySlider || durationInput || participantsInput) {
            [difficultySlider, durationInput, participantsInput].forEach(input => {
                if (input) {
                    input.addEventListener('input', () => {
                        this.calculateExpeditionCost();
                    });
                }
            });
        }
    }

    calculateExpeditionCost() {
        const difficulty = parseInt(document.querySelector('input[name="difficulty_level"]')?.value) || 1;
        const duration = parseInt(document.querySelector('input[name="duration_hours"]')?.value) || 24;
        const participants = parseInt(document.querySelector('input[name="max_participants"]')?.value) || 5;
        
        const baseCost = difficulty * 1000;
        const durationMultiplier = Math.ceil(duration / 24);
        const participantBonus = participants * 500;
        
        const totalCost = baseCost * durationMultiplier + participantBonus;
        
        // Display cost if there's a cost display element
        const costDisplay = document.getElementById('expeditionCost');
        if (costDisplay) {
            costDisplay.textContent = `${totalCost.toLocaleString()} Linh Thạch`;
        }
    }

    setupRequirementChecker() {
        // Check if user meets expedition requirements
        document.addEventListener('click', (e) => {
            if (e.target.matches('.join-expedition-btn')) {
                const expeditionCard = e.target.closest('.expedition-card');
                this.checkRequirements(expeditionCard);
            }
        });
    }

    checkRequirements(expeditionCard) {
        const minCultivation = expeditionCard.querySelector('[data-min-cultivation]')?.textContent;
        const requiredItems = expeditionCard.querySelector('[data-required-items]')?.textContent;
        
        // This would check against user's actual stats
        // For now, just show a notification
        if (minCultivation) {
            window.tuTienApp.showNotification(
                'Yêu Cầu Đạo Lữ', 
                `Cần cảnh giới tối thiểu: ${minCultivation}`, 
                'info'
            );
        }
    }

    setupRewardSystem() {
        // Handle expedition completion rewards
        this.setupRewardDistribution();
        
        // Achievement tracking for expeditions
        this.setupAchievementTracking();
    }

    setupRewardDistribution() {
        // Simulate reward distribution for completed expeditions
        const completedExpeditions = document.querySelectorAll('.expedition-completed');
        completedExpeditions.forEach(expedition => {
            this.processRewards(expedition);
        });
    }

    processRewards(expeditionElement) {
        // Calculate and distribute rewards based on contribution
        const contributionPoints = expeditionElement.querySelector('[data-contribution]')?.textContent || '0';
        const baseReward = parseInt(contributionPoints) * 10;
        
        if (baseReward > 0) {
            setTimeout(() => {
                window.tuTienApp.showNotification(
                    'Phần Thưởng Đạo Lữ', 
                    `Nhận được ${baseReward} linh thạch từ đạo lữ!`, 
                    'success'
                );
            }, Math.random() * 5000);
        }
    }

    setupAchievementTracking() {
        // Track expedition-related achievements
        const userExpeditions = document.querySelectorAll('.user-expedition-item');
        
        if (userExpeditions.length >= 5) {
            window.tuTienApp.showNotification(
                'Thành Tựu Mở Khóa!', 
                'Đạt thành tựu "Đạo Lữ Gia Dày Dạn"', 
                'achievement'
            );
        }
    }

    startExpeditionUpdates() {
        // Start periodic updates for expeditions
        this.expeditionTimer = setInterval(() => {
            this.updateAllExpeditions();
        }, 60000); // Update every minute
    }

    updateAllExpeditions() {
        this.updateActiveExpeditions();
        this.updateAvailableExpeditions();
        this.checkExpeditionCompletion();
    }

    updateActiveExpeditions() {
        const activeExpeditions = document.querySelectorAll('.active-expedition-item');
        activeExpeditions.forEach(expedition => {
            this.updateExpeditionProgress(expedition);
        });
    }

    updateExpeditionProgress(expeditionElement) {
        const progressBar = expeditionElement.querySelector('.progress-bar');
        if (progressBar) {
            const currentWidth = parseFloat(progressBar.style.width) || 0;
            const newWidth = Math.min(currentWidth + Math.random() * 5, 100);
            progressBar.style.width = `${newWidth}%`;
            
            if (newWidth >= 100) {
                this.completeExpedition(expeditionElement);
            }
        }
    }

    completeExpedition(expeditionElement) {
        expeditionElement.classList.add('expedition-completed');
        
        // Show completion effect
        this.showExpeditionCompletionEffect();
        
        // Process rewards
        this.processRewards(expeditionElement);
    }

    showExpeditionCompletionEffect() {
        window.tuTienApp.showNotification(
            'Đạo Lữ Hoàn Thành!', 
            'Một đạo lữ của bạn đã hoàn thành thành công!', 
            'success'
        );
    }

    updateAvailableExpeditions() {
        // Randomly add new expeditions
        if (Math.random() < 0.1) { // 10% chance
            this.addNewExpedition();
        }
    }

    addNewExpedition() {
        const expeditionNames = [
            "Khám Phá Hang Động Bí Ẩn",
            "Tìm Kiếm Thiên Tài Địa Bảo",
            "Săn Lùng Ác Quỷ",
            "Thu Thập Linh Thảo Quý",
            "Khảo Sát Vùng Đất Mới"
        ];
        
        const randomName = expeditionNames[Math.floor(Math.random() * expeditionNames.length)];
        
        window.tuTienApp.showNotification(
            'Đạo Lữ Mới!', 
            `Đạo lữ "${randomName}" vừa được công bố!`, 
            'info'
        );
    }

    checkExpeditionCompletion() {
        // Check for expeditions that should be completed
        const expeditions = document.querySelectorAll('.expedition-item[data-end-time]');
        const now = new Date();
        
        expeditions.forEach(expedition => {
            const endTime = new Date(expedition.dataset.endTime);
            if (now >= endTime && !expedition.classList.contains('completed')) {
                this.completeExpedition(expedition);
            }
        });
    }

    // Cleanup
    destroy() {
        if (this.expeditionTimer) {
            clearInterval(this.expeditionTimer);
        }
    }
}

// Global expedition functions
async function joinExpedition(expeditionId) {
    if (window.expeditionManager) {
        await window.expeditionManager.handleJoinExpedition(expeditionId);
    }
}

function generateRoute() {
    if (window.expeditionManager) {
        window.expeditionManager.generateAIRoute();
    }
}

function updateRangeValue(input, displayId) {
    const display = document.getElementById(displayId);
    if (display) {
        display.textContent = input.value;
    }
    
    // Update route suggestions if this is difficulty slider
    if (input.name === 'difficulty_level' && window.expeditionManager) {
        window.expeditionManager.updateRouteSuggestions(parseInt(input.value));
    }
}

function leaveExpedition(expeditionId) {
    if (confirm('Bạn có chắc muốn rời khỏi đạo lữ này?')) {
        fetch(`/api/leave-expedition/${expeditionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.tuTienApp.showNotification('Rời Đạo Lữ', 'Đã rời khỏi đạo lữ thành công!', 'info');
                location.reload();
            } else {
                window.tuTienApp.showNotification('Lỗi', data.error, 'error');
            }
        })
        .catch(error => {
            window.tuTienApp.showNotification('Lỗi', 'Không thể rời đạo lữ!', 'error');
        });
    }
}

function viewExpeditionDetails(expeditionId) {
    // Implementation for viewing detailed expedition information
    window.tuTienApp.showNotification('Chi Tiết Đạo Lữ', 'Tính năng xem chi tiết sẽ được phát triển!', 'info');
}

// Initialize expedition manager on page load
document.addEventListener('DOMContentLoaded', () => {
    if (document.body.classList.contains('expeditions-page') || window.location.pathname.includes('expeditions')) {
        window.expeditionManager = new ExpeditionManager();
        console.log('Expedition Manager initialized successfully!');
    }
});
