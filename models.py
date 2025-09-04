from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    
    # Tu luyện attributes
    cultivation_level = db.Column(db.String(50), default="Luyện Khí Tầng 1")
    spiritual_power = db.Column(db.Integer, default=100)
    cultivation_points = db.Column(db.Integer, default=0)
    
    # Profile info
    dao_name = db.Column(db.String(100))  # Đạo hiệu
    sect_affiliation = db.Column(db.String(100))
    reputation = db.Column(db.Integer, default=0, nullable=False)
    karma_points = db.Column(db.Integer, default=0, nullable=False)
    
    # Resources
    spiritual_stones = db.Column(db.Integer, default=1000)
    pills_count = db.Column(db.Integer, default=5)
    artifacts_count = db.Column(db.Integer, default=1)
    
    # Mining system
    mining_level = db.Column(db.Integer, default=1, nullable=False)
    mining_experience = db.Column(db.Integer, default=0, nullable=False)
    last_mining = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Free benefits
    free_world_opening_used = db.Column(db.Boolean, default=False)
    
    # Admin privileges
    is_admin = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_cultivation = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))
    owned_worlds = db.relationship('World', backref='owner', lazy=True)
    expedition_participations = db.relationship('ExpeditionParticipant', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_cultivation_stage(self):
        stages = [
            "Luyện Khí", "Trúc Cơ", "Kết Đan", "Nguyên Anh", "Hóa Thần",
            "Luyện Hư", "Hợp Thể", "Đại Thừa", "Độ Kiếp", "Tản Tiên", "Toàn Chi Thiên Đạo"
        ]
        for stage in stages:
            if stage in self.cultivation_level:
                return stage
        return "Luyện Khí"
    
    def get_cultivation_substage(self):
        """Lấy tầng chi tiết (1-9 hoặc Viên Mãn hoặc các cấp đặc biệt)"""
        level = self.cultivation_level
        
        # Kiểm tra các cấp độ đặc biệt của Toàn Chi Thiên Đạo
        if "Đại Viên Mãn" in level:
            return "Đại Viên Mãn"
        elif "Hậu Kỳ" in level:
            return "Hậu Kỳ"
        elif "Trung Kỳ" in level:
            return "Trung Kỳ"
        elif "Sơ Kỳ" in level:
            return "Sơ Kỳ"
        elif "Viên Mãn" in level:
            return "Viên Mãn"
        
        # Tìm tầng số (1-9)
        for i in range(1, 10):
            if f"Tầng {i}" in level:
                return f"Tầng {i}"
        return "Tầng 1"
    
    @property
    def safe_mining_level(self):
        """Trả về mining_level với giá trị mặc định nếu None"""
        return self.mining_level or 1
    
    @property
    def safe_mining_experience(self):
        """Trả về mining_experience với giá trị mặc định nếu None"""
        return self.mining_experience or 0

class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Guild stats
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    treasury = db.Column(db.Integer, default=0)
    territory_count = db.Column(db.Integer, default=1)
    
    # Guild settings
    recruitment_open = db.Column(db.Boolean, default=True)
    min_cultivation_level = db.Column(db.String(50), default="Luyện Khí Tầng 1")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', backref='guild', lazy=True, foreign_keys='User.guild_id')
    wars = db.relationship('GuildWar', backref='guild', lazy=True, foreign_keys='GuildWar.guild_id')
    expeditions = db.relationship('Expedition', backref='organizing_guild', lazy=True)

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    world_type = db.Column(db.String(50))  # Linh Giới, Ma Cảnh, Thiên Giới, etc.
    description = db.Column(db.Text)
    
    # Core World properties
    spiritual_density = db.Column(db.Integer, default=50)  # 0-100
    danger_level = db.Column(db.Integer, default=1)  # 1-10
    resource_richness = db.Column(db.Integer, default=50)  # 0-100
    
    # New Advanced Properties
    world_level = db.Column(db.Integer, default=1)  # Level thế giới
    world_experience = db.Column(db.Integer, default=0)  # Kinh nghiệm thế giới
    stability = db.Column(db.Integer, default=100)  # Độ ổn định (0-100)
    magical_resonance = db.Column(db.Integer, default=50)  # Cộng hưởng ma pháp
    time_flow_rate = db.Column(db.Float, default=1.0)  # Tốc độ thời gian (0.5x - 3.0x)
    gravity_strength = db.Column(db.Float, default=1.0)  # Lực hấp dẫn
    
    # Defensive Systems
    barrier_strength = db.Column(db.Integer, default=0)  # Độ bền kết giới
    guardian_level = db.Column(db.Integer, default=0)  # Level thủ hộ thần
    trap_density = db.Column(db.Integer, default=0)  # Mật độ bẫy
    
    # Economic Systems
    spiritual_stones_production = db.Column(db.Integer, default=100)
    rare_materials_count = db.Column(db.Integer, default=0)
    daily_income = db.Column(db.Integer, default=0)
    trade_routes = db.Column(db.Integer, default=0)  # Số tuyến thương mại
    market_level = db.Column(db.Integer, default=0)  # Cấp độ chợ búa
    
    # Special Resources
    spiritual_herbs = db.Column(db.Integer, default=0)  # Linh thảo
    ancient_artifacts = db.Column(db.Integer, default=0)  # Cổ vật
    essence_crystals = db.Column(db.Integer, default=0)  # Tinh thể tinh hoa
    dragon_scales = db.Column(db.Integer, default=0)  # Vảy rồng
    phoenix_feathers = db.Column(db.Integer, default=0)  # Lông phượng hoàng
    
    # Environmental Features
    climate_control = db.Column(db.Integer, default=0)  # Kiểm soát khí hậu
    terrain_complexity = db.Column(db.Integer, default=1)  # Độ phức tạp địa hình
    ecosystem_diversity = db.Column(db.Integer, default=1)  # Đa dạng sinh thái
    natural_wonders = db.Column(db.Integer, default=0)  # Kỳ quan thiên nhiên
    
    # Cultivation Enhancement
    cultivation_bonus = db.Column(db.Float, default=1.0)  # Bonus tu luyện
    breakthrough_chance = db.Column(db.Float, default=0.1)  # Cơ hội đột phá
    enlightenment_spots = db.Column(db.Integer, default=0)  # Điểm ngộ đạo
    
    # Population and Development
    population_limit = db.Column(db.Integer, default=100)  # Giới hạn dân số
    current_population = db.Column(db.Integer, default=0)  # Dân số hiện tại
    development_level = db.Column(db.Integer, default=1)  # Mức phát triển
    infrastructure_level = db.Column(db.Integer, default=1)  # Cấp cơ sở hạ tầng
    
    # Special Abilities
    dimensional_gate = db.Column(db.Boolean, default=False)  # Cổng không gian
    time_acceleration = db.Column(db.Boolean, default=False)  # Tăng tốc thời gian
    resource_multiplication = db.Column(db.Boolean, default=False)  # Nhân tài nguyên
    auto_cultivation = db.Column(db.Boolean, default=False)  # Tự động tu luyện
    
    # Status and History
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_contested = db.Column(db.Boolean, default=False)
    last_explored = db.Column(db.DateTime)
    last_upgraded = db.Column(db.DateTime)
    total_upgrades = db.Column(db.Integer, default=0)
    
    # Combat and Events
    last_attacked = db.Column(db.DateTime)
    successful_defenses = db.Column(db.Integer, default=0)
    special_events_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_total_power(self):
        """Tính tổng sức mạnh thế giới"""
        base_power = (self.world_level * 1000) + (self.spiritual_density * 10) + (self.resource_richness * 5)
        defensive_power = (self.barrier_strength * 20) + (self.guardian_level * 100) + (self.trap_density * 15)
        special_power = sum([
            self.dimensional_gate * 500,
            self.time_acceleration * 300,
            self.resource_multiplication * 400,
            self.auto_cultivation * 600
        ])
        return base_power + defensive_power + special_power
    
    def get_upgrade_cost(self, upgrade_type):
        """Tính chi phí nâng cấp"""
        base_costs = {
            'spiritual_density': 5000,
            'resource_richness': 5000,
            'world_level': 10000,
            'barrier_strength': 8000,
            'guardian_level': 15000,
            'cultivation_bonus': 12000,
            'dimensional_gate': 50000,
            'time_acceleration': 40000,
            'auto_cultivation': 60000,
            'market_level': 7000,
            'infrastructure': 6000
        }
        
        base_cost = base_costs.get(upgrade_type, 5000)
        level_multiplier = (self.world_level + getattr(self, upgrade_type.replace('_level', ''), 0)) // 2 + 1
        return base_cost * level_multiplier

class GuildWar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'), nullable=False)
    target_guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'), nullable=False)
    
    war_type = db.Column(db.String(50))  # "Sát Nhập", "Chinh Phục", "Liên Minh"
    status = db.Column(db.String(50), default="Đang Diễn Ra")  # Đang Diễn Ra, Hoàn Thành, Thất Bại
    
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    
    # War results
    winner_guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))
    casualties = db.Column(db.Text)  # JSON string
    rewards = db.Column(db.Text)  # JSON string

class Expedition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Expedition details
    destination = db.Column(db.String(100))
    difficulty_level = db.Column(db.Integer, default=1)
    max_participants = db.Column(db.Integer, default=5)
    duration_hours = db.Column(db.Integer, default=24)
    
    # Requirements
    min_cultivation = db.Column(db.String(50))
    required_items = db.Column(db.Text)  # JSON string
    
    # Status
    status = db.Column(db.String(50), default="Tuyển Thành Viên")
    organizer_guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'))
    start_time = db.Column(db.DateTime)
    
    # Rewards
    potential_rewards = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('ExpeditionParticipant', backref='expedition', lazy=True)

class ExpeditionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expedition_id = db.Column(db.Integer, db.ForeignKey('expedition.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Chờ Xác Nhận")
    contribution_points = db.Column(db.Integer, default=0)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    channel = db.Column(db.String(50), default="general")  # general, guild, expedition
    channel_id = db.Column(db.Integer)  # ID of guild or expedition
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='messages', lazy=True)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # cultivation, guild, expedition, etc.
    rarity = db.Column(db.String(20), default="common")  # common, rare, legendary
    
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='achievements', lazy=True)
