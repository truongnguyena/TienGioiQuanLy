// Enhanced Guild Management System
class GuildManager {
    constructor() {
        this.currentGuild = null;
        this.guildMembers = [];
        this.guildWars = [];
        this.init();
    }

    init() {
        this.setupGuildEvents();
        this.loadGuildData();
        this.setupRealTimeUpdates();
    }

    setupGuildEvents() {
        // Guild creation
        const createGuildBtn = document.getElementById('createGuildBtn');
        if (createGuildBtn) {
            createGuildBtn.addEventListener('click', () => this.showCreateGuildModal());
        }

        // Guild join
        const joinGuildBtn = document.getElementById('joinGuildBtn');
        if (joinGuildBtn) {
            joinGuildBtn.addEventListener('click', () => this.showJoinGuildModal());
        }

        // Guild settings
        const guildSettingsBtn = document.getElementById('guildSettingsBtn');
        if (guildSettingsBtn) {
            guildSettingsBtn.addEventListener('click', () => this.showGuildSettingsModal());
        }

        // Guild war
        const declareWarBtn = document.getElementById('declareWarBtn');
        if (declareWarBtn) {
            declareWarBtn.addEventListener('click', () => this.showDeclareWarModal());
        }
    }

    async loadGuildData() {
        try {
            const response = await fetch('/api/guild/data');
            if (response.ok) {
                const data = await response.json();
                this.currentGuild = data.guild;
                this.guildMembers = data.members || [];
                this.guildWars = data.wars || [];
                this.updateGuildUI();
            }
        } catch (error) {
            console.error('Error loading guild data:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi tải dữ liệu guild', 'error');
            }
        }
    }

    updateGuildUI() {
        this.updateGuildInfo();
        this.updateGuildMembers();
        this.updateGuildWars();
        this.updateGuildTreasury();
    }

    updateGuildInfo() {
        if (!this.currentGuild) return;

        // Update guild name
        const guildNameEl = document.getElementById('guildName');
        if (guildNameEl) {
            guildNameEl.textContent = this.currentGuild.name;
        }

        // Update guild level
        const guildLevelEl = document.getElementById('guildLevel');
        if (guildLevelEl) {
            guildLevelEl.textContent = `Cấp ${this.currentGuild.level}`;
        }

        // Update guild description
        const guildDescEl = document.getElementById('guildDescription');
        if (guildDescEl) {
            guildDescEl.textContent = this.currentGuild.description || 'Chưa có mô tả';
        }

        // Update member count
        const memberCountEl = document.getElementById('memberCount');
        if (memberCountEl) {
            memberCountEl.textContent = `${this.guildMembers.length} thành viên`;
        }
    }

    updateGuildMembers() {
        const membersContainer = document.getElementById('guildMembersList');
        if (!membersContainer) return;

        membersContainer.innerHTML = '';

        this.guildMembers.forEach(member => {
            const memberEl = this.createMemberElement(member);
            membersContainer.appendChild(memberEl);
        });
    }

    createMemberElement(member) {
        const memberEl = document.createElement('div');
        memberEl.className = 'guild-member-item';
        memberEl.innerHTML = `
            <div class="member-avatar">
                <i class="fas fa-user-circle"></i>
            </div>
            <div class="member-info">
                <h6 class="member-name">${member.dao_name || member.username}</h6>
                <p class="member-level">${member.cultivation_level}</p>
                <p class="member-role">${member.role || 'Thành viên'}</p>
            </div>
            <div class="member-actions">
                ${member.role === 'Leader' ? '' : `
                    <button class="btn btn-sm btn-outline-danger" onclick="guildManager.kickMember(${member.id})">
                        <i class="fas fa-user-times"></i>
                    </button>
                `}
            </div>
        `;
        return memberEl;
    }

    updateGuildWars() {
        const warsContainer = document.getElementById('guildWarsList');
        if (!warsContainer) return;

        warsContainer.innerHTML = '';

        this.guildWars.forEach(war => {
            const warEl = this.createWarElement(war);
            warsContainer.appendChild(warEl);
        });
    }

    createWarElement(war) {
        const warEl = document.createElement('div');
        warEl.className = 'guild-war-item';
        warEl.innerHTML = `
            <div class="war-info">
                <h6 class="war-title">${war.war_type} - ${war.target_guild_name}</h6>
                <p class="war-status">Trạng thái: ${war.status}</p>
                <p class="war-time">Bắt đầu: ${new Date(war.start_time).toLocaleString()}</p>
            </div>
            <div class="war-actions">
                <button class="btn btn-sm btn-primary" onclick="guildManager.viewWarDetails(${war.id})">
                    <i class="fas fa-eye"></i> Chi tiết
                </button>
            </div>
        `;
        return warEl;
    }

    updateGuildTreasury() {
        if (!this.currentGuild) return;

        const treasuryEl = document.getElementById('guildTreasury');
        if (treasuryEl) {
            treasuryEl.textContent = `${this.currentGuild.treasury.toLocaleString()} Linh Thạch`;
        }
    }

    showCreateGuildModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content mystical-card">
                    <div class="modal-header">
                        <h5 class="modal-title">Tạo Guild Mới</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="createGuildForm">
                            <div class="mb-3">
                                <label for="guildName" class="form-label">Tên Guild</label>
                                <input type="text" class="form-control" id="guildName" required>
                            </div>
                            <div class="mb-3">
                                <label for="guildDescription" class="form-label">Mô tả</label>
                                <textarea class="form-control" id="guildDescription" rows="3"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="minCultivationLevel" class="form-label">Cấp độ tu luyện tối thiểu</label>
                                <select class="form-select" id="minCultivationLevel">
                                    <option value="Luyện Khí Tầng 1">Luyện Khí Tầng 1</option>
                                    <option value="Luyện Khí Tầng 5">Luyện Khí Tầng 5</option>
                                    <option value="Trúc Cơ Tầng 1">Trúc Cơ Tầng 1</option>
                                    <option value="Kết Đan Tầng 1">Kết Đan Tầng 1</option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Hủy</button>
                        <button type="button" class="btn btn-primary" onclick="guildManager.createGuild()">Tạo Guild</button>
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

    async createGuild() {
        const form = document.getElementById('createGuildForm');
        const formData = new FormData(form);
        
        const guildData = {
            name: formData.get('guildName') || document.getElementById('guildName').value,
            description: formData.get('guildDescription') || document.getElementById('guildDescription').value,
            min_cultivation_level: formData.get('minCultivationLevel') || document.getElementById('minCultivationLevel').value
        };

        try {
            const response = await fetch('/api/guild/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(guildData)
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Tạo guild thành công!', 'success');
                }
                this.loadGuildData();
                bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            } else {
                throw new Error(result.error || 'Tạo guild thất bại');
            }
        } catch (error) {
            console.error('Error creating guild:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi tạo guild: ' + error.message, 'error');
            }
        }
    }

    showJoinGuildModal() {
        // Load available guilds
        this.loadAvailableGuilds().then(guilds => {
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content mystical-card">
                        <div class="modal-header">
                            <h5 class="modal-title">Tham Gia Guild</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="guild-list">
                                ${guilds.map(guild => `
                                    <div class="guild-item" onclick="guildManager.selectGuild(${guild.id})">
                                        <h6>${guild.name}</h6>
                                        <p>${guild.description || 'Chưa có mô tả'}</p>
                                        <small>Cấp ${guild.level} - ${guild.member_count} thành viên</small>
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
        });
    }

    async loadAvailableGuilds() {
        try {
            const response = await fetch('/api/guild/available');
            if (response.ok) {
                const data = await response.json();
                return data.guilds || [];
            }
        } catch (error) {
            console.error('Error loading available guilds:', error);
        }
        return [];
    }

    async selectGuild(guildId) {
        try {
            const response = await fetch('/api/guild/join', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ guild_id: guildId })
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Tham gia guild thành công!', 'success');
                }
                this.loadGuildData();
                bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            } else {
                throw new Error(result.error || 'Tham gia guild thất bại');
            }
        } catch (error) {
            console.error('Error joining guild:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi tham gia guild: ' + error.message, 'error');
            }
        }
    }

    async kickMember(memberId) {
        if (!confirm('Bạn có chắc muốn đuổi thành viên này?')) return;

        try {
            const response = await fetch('/api/guild/kick', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ member_id: memberId })
            });

            const result = await response.json();

            if (result.success) {
                if (window.enhancedUI) {
                    window.enhancedUI.showNotification('Đã đuổi thành viên', 'success');
                }
                this.loadGuildData();
            } else {
                throw new Error(result.error || 'Đuổi thành viên thất bại');
            }
        } catch (error) {
            console.error('Error kicking member:', error);
            if (window.enhancedUI) {
                window.enhancedUI.showNotification('Lỗi đuổi thành viên: ' + error.message, 'error');
            }
        }
    }

    setupRealTimeUpdates() {
        // Update guild data every 30 seconds
        setInterval(() => {
            if (this.currentGuild) {
                this.loadGuildData();
            }
        }, 30000);
    }
}

// Initialize Guild Manager
document.addEventListener('DOMContentLoaded', () => {
    window.guildManager = new GuildManager();
});
