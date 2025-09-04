#!/usr/bin/env python3
"""
Initialize production database with optimizations
"""
import os
import sys
from app import app, db
from models import User, Guild, World, GuildWar, Expedition, ExpeditionParticipant, ChatMessage, Achievement
from db_optimizer import DatabaseOptimizer

def init_production_database():
    """Initialize production database with all tables and optimizations"""
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            
            print("Creating database indexes...")
            DatabaseOptimizer.optimize_user_queries(db)
            
            print("Creating sample data...")
            
            # Create a sample admin user
            admin_user = User(
                username='admin',
                email='admin@tiengioi.com',
                cultivation_level='Đại Thừa Tầng 9',
                spiritual_power=10000,
                cultivation_points=50000,
                dao_name='Thiên Đế',
                sect_affiliation='Thiên Môn',
                reputation=10000,
                karma_points=5000,
                spiritual_stones=100000,
                pills_count=100,
                artifacts_count=50,
                is_admin=True
            )
            admin_user.set_password('admin123')
            
            # Check if admin already exists
            if not User.query.filter_by(username='admin').first():
                db.session.add(admin_user)
                print("Created admin user: admin/admin123")
            
            # Create a sample guild
            if not Guild.query.filter_by(name='Thiên Môn').first():
                sample_guild = Guild(
                    name='Thiên Môn',
                    description='Guild mạnh nhất trong thiên hạ',
                    leader_id=admin_user.id if admin_user.id else 1,
                    level=10,
                    experience=50000,
                    treasury=100000,
                    territory_count=5,
                    recruitment_open=True,
                    min_cultivation_level='Kết Đan Tầng 1'
                )
                db.session.add(sample_guild)
                print("Created sample guild: Thiên Môn")
            
            # Create sample worlds
            if not World.query.filter_by(name='Linh Giới Cổ').first():
                sample_worlds = [
                    World(
                        name='Linh Giới Cổ',
                        world_type='Linh Giới',
                        description='Thế giới cổ đại với mật độ linh khí cao',
                        spiritual_density=90,
                        resource_richness=85,
                        danger_level=5,
                        world_level=8,
                        spiritual_stones_production=500,
                        owner_id=admin_user.id if admin_user.id else 1
                    ),
                    World(
                        name='Ma Cảnh U Minh',
                        world_type='Ma Cảnh',
                        description='Thế giới ma quỷ đầy nguy hiểm',
                        spiritual_density=70,
                        resource_richness=60,
                        danger_level=8,
                        world_level=6,
                        spiritual_stones_production=300,
                        owner_id=admin_user.id if admin_user.id else 1
                    ),
                    World(
                        name='Thiên Giới Thánh Địa',
                        world_type='Thiên Giới',
                        description='Thế giới thiên thần với năng lượng thánh',
                        spiritual_density=95,
                        resource_richness=90,
                        danger_level=3,
                        world_level=10,
                        spiritual_stones_production=800,
                        owner_id=admin_user.id if admin_user.id else 1
                    )
                ]
                
                for world in sample_worlds:
                    db.session.add(world)
                print("Created sample worlds")
            
            # Create sample achievements
            if not Achievement.query.first():
                sample_achievements = [
                    Achievement(
                        user_id=admin_user.id if admin_user.id else 1,
                        title='Thiên Tài Tu Luyện',
                        description='Đạt được cấp độ Đại Thừa',
                        category='cultivation',
                        rarity='legendary'
                    ),
                    Achievement(
                        user_id=admin_user.id if admin_user.id else 1,
                        title='Chủ Nhân Thế Giới',
                        description='Sở hữu nhiều thế giới',
                        category='world',
                        rarity='rare'
                    ),
                    Achievement(
                        user_id=admin_user.id if admin_user.id else 1,
                        title='Lãnh Đạo Guild',
                        description='Thành lập guild thành công',
                        category='guild',
                        rarity='common'
                    )
                ]
                
                for achievement in sample_achievements:
                    db.session.add(achievement)
                print("Created sample achievements")
            
            db.session.commit()
            print("Production database initialized successfully!")
            print("Admin credentials: admin/admin123")
            
        except Exception as e:
            print(f"Database initialization failed: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == "__main__":
    init_production_database()
