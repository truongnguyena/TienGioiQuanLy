
from app import app, db
from models import User, Guild, World, GuildWar, Expedition, ExpeditionParticipant, ChatMessage, Achievement

def init_database():
    """Initialize database with all tables"""
    with app.app_context():
        try:
            # Drop all tables and recreate
            db.drop_all()
            db.create_all()
            
            # Create a sample world for testing
            sample_world = World(
                name="Linh Giới Cổ",
                world_type="Linh Giới",
                description="Một thế giới cổ đại với mật độ linh khí cao",
                spiritual_density=80,
                resource_richness=75,
                danger_level=3,
                spiritual_stones_production=200
            )
            
            db.session.add(sample_world)
            db.session.commit()
            
            print("Database initialized successfully!")
            print("Sample world created: Linh Giới Cổ")
            
        except Exception as e:
            print(f"Database initialization failed: {e}")
            db.session.rollback()

if __name__ == "__main__":
    init_database()
