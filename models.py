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
    reputation = db.Column(db.Integer, default=0)
    karma_points = db.Column(db.Integer, default=0)
    
    # Resources
    spiritual_stones = db.Column(db.Integer, default=1000)
    pills_count = db.Column(db.Integer, default=5)
    artifacts_count = db.Column(db.Integer, default=1)
    
    # Mining system
    mining_level = db.Column(db.Integer, default=1)
    mining_experience = db.Column(db.Integer, default=0)
    last_mining = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Free benefits
    free_world_opening_used = db.Column(db.Boolean, default=False)
    
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
            "Luyện Hư", "Hợp Thể", "Đại Thừa", "Độ Kiếp", "Tản Tiên"
        ]
        for stage in stages:
            if stage in self.cultivation_level:
                return stage
        return "Luyện Khí"

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
    
    # World properties
    spiritual_density = db.Column(db.Integer, default=50)  # 0-100
    danger_level = db.Column(db.Integer, default=1)  # 1-10
    resource_richness = db.Column(db.Integer, default=50)  # 0-100
    
    # Resources
    spiritual_stones_production = db.Column(db.Integer, default=100)
    rare_materials_count = db.Column(db.Integer, default=0)
    
    # Status
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_contested = db.Column(db.Boolean, default=False)
    last_explored = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
