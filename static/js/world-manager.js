// Enhanced World Management System
class WorldManager {
    constructor() {
        this.ownedWorlds = [];
        this.availableWorlds = [];
        this.currentWorld = null;
        this.init();
    }

    init() {
        this.setupWorldEvents();
        this.loadWorldData();
        this.setupRealTimeUpdates();
    }

    setupWorldEvents() {
        // World creation
        const createWorldBtn = document.getElementById('createWorldBtn');
        if (createWorldBtn) {
            createWorldBtn.addEventListener('click', () => this.showCreateWorldModal());
        }

        // World upgrade
        const upgradeWorldBtn = document.getElementById('upgradeWorldBtn');
        if (upgradeWorldBtn) {
            upgradeWorldBtn.addEventListener('click', () => this.showUpgradeWorldModal());
        }

        // World exploration
        const exploreWorldBtn = document.getElementById('exploreWorldBtn');
        if (exploreWorldBtn) {
            exploreWorldBtn.addEventListener('click', () => this.exploreWorld());
        }
    }

    async loadWorldData() {
        try {
            const response = await fetch('/api/world/data');
            if (response.ok) {
                const data = await response.json();
                this.ownedWorlds = data.owned_worlds || [];
                this.availableWorlds = data.available_worlds || [];
                this.updateWorldUI();
            }
        } catch (error) {
            console.error('Error loading world data:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi tải dữ liệu thế giới', 'error');
            }
        }
    }

    updateWorldUI() {
        this.updateOwnedWorlds();
        this.updateAvailableWorlds();
        this.updateWorldStats();
    }

    updateOwnedWorlds() {
        const worldsContainer = document.getElementById('ownedWorldsList');
        if (!worldsContainer) return;

        worldsContainer.innerHTML = '';

        this.ownedWorlds.forEach(world => {
            const worldEl = this.createWorldElement(world, true);
            worldsContainer.appendChild(worldEl);
        });
    }

    updateAvailableWorlds() {
        const worldsContainer = document.getElementById('availableWorldsList');
        if (!worldsContainer) return;

        worldsContainer.innerHTML = '';

        this.availableWorlds.forEach(world => {
            const worldEl = this.createWorldElement(world, false);
            worldsContainer.appendChild(worldEl);
        });
    }

    createWorldElement(world, isOwned) {
        const worldEl = document.createElement('div');
        worldEl.className = 'world-item';
        worldEl.innerHTML = `
            <div class="world-header">
                <h5 class="world-name">${world.name}</h5>
                <span class="world-type badge bg-primary">${world.world_type}</span>
            </div>
            <div class="world-stats">
                <div class="stat-item">
                    <i class="fas fa-level-up-alt"></i>
                    <span>Cấp ${world.world_level}</span>
                </div>
                <div class="stat-item">
                    <i class="fas fa-gem"></i>
                    <span>${world.spiritual_density}%</span>
                </div>
                <div class="stat-item">
                    <i class="fas fa-shield-alt"></i>
                    <span>${world.danger_level}/10</span>
                </div>
            </div>
            <div class="world-description">
                <p>${world.description || 'Chưa có mô tả'}</p>
            </div>
            <div class="world-actions">
                ${isOwned ? `
                    <button class="btn btn-sm btn-primary" onclick="worldManager.manageWorld(${world.id})">
                        <i class="fas fa-cog"></i> Quản lý
                    </button>
                    <button class="btn btn-sm btn-success" onclick="worldManager.upgradeWorld(${world.id})">
                        <i class="fas fa-arrow-up"></i> Nâng cấp
                    </button>
                ` : `
                    <button class="btn btn-sm btn-warning" onclick="worldManager.claimWorld(${world.id})">
                        <i class="fas fa-hand-paper"></i> Chiếm lấy
                    </button>
                `}
            </div>
        `;
        return worldEl;
    }

    updateWorldStats() {
        const totalWorldsEl = document.getElementById('totalWorlds');
        if (totalWorldsEl) {
            totalWorldsEl.textContent = this.ownedWorlds.length;
        }

        const totalResourcesEl = document.getElementById('totalResources');
        if (totalResourcesEl) {
            const totalResources = this.ownedWorlds.reduce((sum, world) => 
                sum + (world.spiritual_stones_production || 0), 0);
            totalResourcesEl.textContent = totalResources.toLocaleString();
        }
    }

    showCreateWorldModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content mystical-card">
                    <div class="modal-header">
                        <h5 class="modal-title">Tạo Thế Giới Mới</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="createWorldForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="worldName" class="form-label">Tên Thế Giới</label>
                                        <input type="text" class="form-control" id="worldName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="worldType" class="form-label">Loại Thế Giới</label>
                                        <select class="form-select" id="worldType" required>
                                            <option value="Linh Giới">Linh Giới</option>
                                            <option value="Ma Cảnh">Ma Cảnh</option>
                                            <option value="Thiên Giới">Thiên Giới</option>
                                            <option value="Huyền Giới">Huyền Giới</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="worldDescription" class="form-label">Mô tả</label>
                                        <textarea class="form-control" id="worldDescription" rows="3"></textarea>
                                    </div>
                                    <div class="mb-3">
                                        <label for="worldLevel" class="form-label">Cấp độ ban đầu</label>
                                        <select class="form-select" id="worldLevel">
                                            <option value="1">Cấp 1</option>
                                            <option value="2">Cấp 2</option>
                                            <option value="3">Cấp 3</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
                        <button type="button" class="btn btn-primary" onclick="worldManager.createWorld()">Tạo Thế Giới</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    async createWorld() {
        const worldData = {
            name: document.getElementById('worldName').value,
            world_type: document.getElementById('worldType').value,
            description: document.getElementById('worldDescription').value,
            world_level: parseInt(document.getElementById('worldLevel').value)
        };

        try {
            const response = await fetch('/api/world/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(worldData)
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Tạo thế giới thành công!', 'success');
                }
                this.loadWorldData();
                bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            } else {
                throw new Error(result.error || 'Tạo thế giới thất bại');
            }
        } catch (error) {
            console.error('Error creating world:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi tạo thế giới: ' + error.message, 'error');
            }
        }
    }

    async manageWorld(worldId) {
        const world = this.ownedWorlds.find(w => w.id === worldId);
        if (!world) return;

        this.currentWorld = world;
        this.showWorldManagementModal();
    }

    showWorldManagementModal() {
        if (!this.currentWorld) return;

        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content mystical-card">
                    <div class="modal-header">
                        <h5 class="modal-title">Quản Lý Thế Giới: ${this.currentWorld.name}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Thông Tin Cơ Bản</h6>
                                <p><strong>Loại:</strong> ${this.currentWorld.world_type}</p>
                                <p><strong>Cấp độ:</strong> ${this.currentWorld.world_level}</p>
                                <p><strong>Mô tả:</strong> ${this.currentWorld.description || 'Chưa có mô tả'}</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Thống Kê</h6>
                                <p><strong>Mật độ linh khí:</strong> ${this.currentWorld.spiritual_density}%</p>
                                <p><strong>Mức độ nguy hiểm:</strong> ${this.currentWorld.danger_level}/10</p>
                                <p><strong>Sản xuất linh thạch:</strong> ${this.currentWorld.spiritual_stones_production}/ngày</p>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-12">
                                <h6>Nâng Cấp</h6>
                                <div class="upgrade-options">
                                    <button class="btn btn-outline-primary" onclick="worldManager.upgradeAttribute('spiritual_density')">
                                        Nâng cấp mật độ linh khí
                                    </button>
                                    <button class="btn btn-outline-success" onclick="worldManager.upgradeAttribute('world_level')">
                                        Nâng cấp cấp độ thế giới
                                    </button>
                                    <button class="btn btn-outline-warning" onclick="worldManager.upgradeAttribute('spiritual_stones_production')">
                                        Nâng cấp sản xuất linh thạch
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    async upgradeAttribute(attribute) {
        if (!this.currentWorld) return;

        try {
            const response = await fetch('/api/world/upgrade', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    world_id: this.currentWorld.id,
                    attribute: attribute
                })
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Nâng cấp thành công!', 'success');
                }
                this.loadWorldData();
            } else {
                throw new Error(result.error || 'Nâng cấp thất bại');
            }
        } catch (error) {
            console.error('Error upgrading world:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi nâng cấp: ' + error.message, 'error');
            }
        }
    }

    async exploreWorld() {
        if (!this.currentWorld) return;

        try {
            const response = await fetch('/api/world/explore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    world_id: this.currentWorld.id
                })
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Khám phá thành công!', 'success');
                }
                this.showExplorationResults(result.results);
            } else {
                throw new Error(result.error || 'Khám phá thất bại');
            }
        } catch (error) {
            console.error('Error exploring world:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi khám phá: ' + error.message, 'error');
            }
        }
    }

    showExplorationResults(results) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content mystical-card">
                    <div class="modal-header">
                        <h5 class="modal-title">Kết Quả Khám Phá</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="exploration-results">
                            ${results.map(result => `
                                <div class="result-item">
                                    <i class="fas fa-${result.icon}"></i>
                                    <span>${result.description}</span>
                                    <span class="result-value">+${result.value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    setupRealTimeUpdates() {
        // Update world data every 60 seconds
        setInterval(() => {
            this.loadWorldData();
        }, 60000);
    }
}

// Initialize World Manager
document.addEventListener('DOMContentLoaded', () => {
    window.worldManager = new WorldManager();
});
