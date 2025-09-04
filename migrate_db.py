
from app import app, db
from models import World
from sqlalchemy import text

def migrate_database():
    """Migrate database to add new columns to World table"""
    with app.app_context():
        try:
            # List of all new columns that need to be added
            new_columns = [
                'world_level INTEGER DEFAULT 1',
                'world_experience INTEGER DEFAULT 0',
                'stability INTEGER DEFAULT 100',
                'magical_resonance INTEGER DEFAULT 50',
                'time_flow_rate FLOAT DEFAULT 1.0',
                'gravity_strength FLOAT DEFAULT 1.0',
                'barrier_strength INTEGER DEFAULT 0',
                'guardian_level INTEGER DEFAULT 0',
                'trap_density INTEGER DEFAULT 0',
                'daily_income INTEGER DEFAULT 0',
                'trade_routes INTEGER DEFAULT 0',
                'market_level INTEGER DEFAULT 0',
                'spiritual_herbs INTEGER DEFAULT 0',
                'ancient_artifacts INTEGER DEFAULT 0',
                'essence_crystals INTEGER DEFAULT 0',
                'dragon_scales INTEGER DEFAULT 0',
                'phoenix_feathers INTEGER DEFAULT 0',
                'climate_control INTEGER DEFAULT 0',
                'terrain_complexity INTEGER DEFAULT 1',
                'ecosystem_diversity INTEGER DEFAULT 1',
                'natural_wonders INTEGER DEFAULT 0',
                'cultivation_bonus FLOAT DEFAULT 1.0',
                'breakthrough_chance FLOAT DEFAULT 0.1',
                'enlightenment_spots INTEGER DEFAULT 0',
                'population_limit INTEGER DEFAULT 100',
                'current_population INTEGER DEFAULT 0',
                'development_level INTEGER DEFAULT 1',
                'infrastructure_level INTEGER DEFAULT 1',
                'dimensional_gate BOOLEAN DEFAULT FALSE',
                'time_acceleration BOOLEAN DEFAULT FALSE',
                'resource_multiplication BOOLEAN DEFAULT FALSE',
                'auto_cultivation BOOLEAN DEFAULT FALSE',
                'last_explored DATETIME',
                'last_upgraded DATETIME',
                'total_upgrades INTEGER DEFAULT 0',
                'last_attacked DATETIME',
                'successful_defenses INTEGER DEFAULT 0',
                'special_events_count INTEGER DEFAULT 0'
            ]
            
            # Add each column if it doesn't exist
            for column_def in new_columns:
                column_name = column_def.split()[0]
                try:
                    # Try to add the column
                    db.session.execute(text(f'ALTER TABLE world ADD COLUMN {column_def}'))
                    db.session.commit()
                    print(f"Added column: {column_name}")
                except Exception as e:
                    if "already exists" in str(e) or "duplicate column" in str(e).lower():
                        print(f"Column {column_name} already exists, skipping...")
                        db.session.rollback()
                    else:
                        print(f"Error adding column {column_name}: {e}")
                        db.session.rollback()
            
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Migration failed: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_database()
