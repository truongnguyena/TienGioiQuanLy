from app import app, db
from sqlalchemy import text

def migrate_user_database():
    """Migrate database to add missing columns to User table"""
    with app.app_context():
        try:
            # List of columns that might be missing from User table
            user_columns = [
                'is_admin BOOLEAN DEFAULT FALSE',
                'guild_id INTEGER',
                'last_cultivation DATETIME',
                'created_at DATETIME',
                'free_world_opening_used BOOLEAN DEFAULT FALSE',
                'mining_level INTEGER DEFAULT 1',
                'mining_experience INTEGER DEFAULT 0',
                'last_mining DATETIME',
                'artifacts_count INTEGER DEFAULT 1',
                'pills_count INTEGER DEFAULT 5',
                'spiritual_stones INTEGER DEFAULT 1000',
                'karma_points INTEGER DEFAULT 0',
                'reputation INTEGER DEFAULT 0',
                'sect_affiliation VARCHAR(100)',
                'dao_name VARCHAR(100)',
                'cultivation_points INTEGER DEFAULT 0',
                'spiritual_power INTEGER DEFAULT 100',
                'cultivation_level VARCHAR(50) DEFAULT "Luyện Khí Tầng 1"'
            ]
            
            # Add each column if it doesn't exist
            for column_def in user_columns:
                column_name = column_def.split()[0]
                try:
                    # Try to add the column
                    db.session.execute(text(f'ALTER TABLE user ADD COLUMN {column_def}'))
                    db.session.commit()
                    print(f"Added column: {column_name}")
                except Exception as e:
                    if "already exists" in str(e) or "duplicate column" in str(e).lower():
                        print(f"Column {column_name} already exists, skipping...")
                        db.session.rollback()
                    else:
                        print(f"Error adding column {column_name}: {e}")
                        db.session.rollback()
            
            print("User database migration completed successfully!")
            
        except Exception as e:
            print(f"User migration failed: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_user_database()
