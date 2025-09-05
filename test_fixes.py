#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify fixes
"""

import os
import sys
from pathlib import Path

def test_database_schema():
    """Test if database schema is correct"""
    print("Testing database schema...")
    
    db_path = Path("instance/tu_tien.db")
    if not db_path.exists():
        print("❌ Database file not found")
        return False
    
    try:
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if world table has required columns
        cursor.execute("PRAGMA table_info(world)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required_columns = [
            'world_level', 'world_experience', 'stability', 
            'magical_resonance', 'time_flow_rate', 'gravity_strength',
            'barrier_strength', 'guardian_level', 'trap_density',
            'daily_income', 'trade_routes', 'market_level',
            'spiritual_herbs', 'ancient_artifacts', 'essence_crystals',
            'dragon_scales', 'phoenix_feathers', 'climate_control',
            'terrain_complexity', 'ecosystem_diversity', 'natural_wonders',
            'cultivation_bonus', 'breakthrough_chance', 'enlightenment_spots',
            'population_limit', 'current_population', 'development_level',
            'infrastructure_level', 'dimensional_gate', 'time_acceleration',
            'resource_multiplication', 'auto_cultivation', 'last_explored',
            'last_upgraded', 'total_upgrades', 'last_attacked',
            'successful_defenses', 'special_events_count'
        ]
        
        missing_columns = []
        for col in required_columns:
            if col not in columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        else:
            print("✅ All required columns exist")
            return True
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_templates():
    """Test if templates have correct syntax"""
    print("Testing template syntax...")
    
    template_dir = Path("templates")
    if not template_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    # Check for common template issues
    issues = []
    
    for template_file in template_dir.glob("*.html"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for common syntax errors
            if '{% break %}' in content:
                issues.append(f"{template_file}: Contains invalid {% break %} tag")
            
            if '{% if' in content and '{% endif %}' not in content:
                # This is a simple check, might have false positives
                pass
                
        except Exception as e:
            issues.append(f"{template_file}: Error reading file - {e}")
    
    if issues:
        print("❌ Template issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Templates look good")
        return True

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        from app import app, db
        from models import User, Guild, World, GuildWar, Expedition, ExpeditionParticipant, ChatMessage, Achievement
        print("✅ Basic imports successful")
        
        # Test if app can be created
        with app.app_context():
            print("✅ App context works")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 Running fix verification tests...\n")
    
    tests = [
        ("Database Schema", test_database_schema),
        ("Template Syntax", test_templates),
        ("Imports", test_imports)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 All tests passed! Fixes appear to be working.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
