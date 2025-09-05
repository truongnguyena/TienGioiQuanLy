#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to fix database schema issues
"""

import sqlite3
import os
from pathlib import Path

def fix_database():
    """Fix database schema by adding missing columns"""
    
    # Find database file
    db_path = Path("instance/tu_tien.db")
    if not db_path.exists():
        print("Database file not found. Creating new database...")
        return
    
    print(f"Found database at: {db_path}")
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # List of columns to add
    columns_to_add = [
        ('world_level', 'INTEGER DEFAULT 1'),
        ('world_experience', 'INTEGER DEFAULT 0'),
        ('stability', 'INTEGER DEFAULT 100'),
        ('magical_resonance', 'INTEGER DEFAULT 50'),
        ('time_flow_rate', 'FLOAT DEFAULT 1.0'),
        ('gravity_strength', 'FLOAT DEFAULT 1.0'),
        ('barrier_strength', 'INTEGER DEFAULT 0'),
        ('guardian_level', 'INTEGER DEFAULT 0'),
        ('trap_density', 'INTEGER DEFAULT 0'),
        ('daily_income', 'INTEGER DEFAULT 0'),
        ('trade_routes', 'INTEGER DEFAULT 0'),
        ('market_level', 'INTEGER DEFAULT 0'),
        ('spiritual_herbs', 'INTEGER DEFAULT 0'),
        ('ancient_artifacts', 'INTEGER DEFAULT 0'),
        ('essence_crystals', 'INTEGER DEFAULT 0'),
        ('dragon_scales', 'INTEGER DEFAULT 0'),
        ('phoenix_feathers', 'INTEGER DEFAULT 0'),
        ('climate_control', 'INTEGER DEFAULT 0'),
        ('terrain_complexity', 'INTEGER DEFAULT 1'),
        ('ecosystem_diversity', 'INTEGER DEFAULT 1'),
        ('natural_wonders', 'INTEGER DEFAULT 0'),
        ('cultivation_bonus', 'FLOAT DEFAULT 1.0'),
        ('breakthrough_chance', 'FLOAT DEFAULT 0.1'),
        ('enlightenment_spots', 'INTEGER DEFAULT 0'),
        ('population_limit', 'INTEGER DEFAULT 100'),
        ('current_population', 'INTEGER DEFAULT 0'),
        ('development_level', 'INTEGER DEFAULT 1'),
        ('infrastructure_level', 'INTEGER DEFAULT 1'),
        ('dimensional_gate', 'BOOLEAN DEFAULT 0'),
        ('time_acceleration', 'BOOLEAN DEFAULT 0'),
        ('resource_multiplication', 'BOOLEAN DEFAULT 0'),
        ('auto_cultivation', 'BOOLEAN DEFAULT 0'),
        ('last_explored', 'DATETIME'),
        ('last_upgraded', 'DATETIME'),
        ('total_upgrades', 'INTEGER DEFAULT 0'),
        ('last_attacked', 'DATETIME'),
        ('successful_defenses', 'INTEGER DEFAULT 0'),
        ('special_events_count', 'INTEGER DEFAULT 0')
    ]
    
    # Check if world table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='world'")
    if not cursor.fetchone():
        print("World table does not exist. Please run init_db.py first.")
        return
    
    # Add missing columns
    for column_name, column_type in columns_to_add:
        try:
            # Check if column already exists
            cursor.execute(f"PRAGMA table_info(world)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE world ADD COLUMN {column_name} {column_type}")
                print(f"Added column: {column_name}")
            else:
                print(f"Column {column_name} already exists, skipping...")
                
        except Exception as e:
            print(f"Error adding column {column_name}: {e}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database migration completed successfully!")

if __name__ == "__main__":
    fix_database()
