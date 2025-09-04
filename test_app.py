#!/usr/bin/env python3
"""
Test script to verify application functionality before deployment
"""
import os
import sys
from app import app, db, cache
from models import User, Guild, World, Achievement
from db_optimizer import DatabaseOptimizer

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_login import LoginManager
        from flask_caching import Cache
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        with app.app_context():
            # Test basic query
            user_count = User.query.count()
            print(f"✅ Database connection successful. Users: {user_count}")
            return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_database_optimizer():
    """Test DatabaseOptimizer functionality"""
    print("Testing DatabaseOptimizer...")
    try:
        with app.app_context():
            # Test user stats
            user_stats = DatabaseOptimizer.get_user_stats(db, cache)
            print(f"✅ User stats: {user_stats}")
            
            # Test guild stats
            guild_stats = DatabaseOptimizer.get_guild_stats(db, cache)
            print(f"✅ Guild stats: {guild_stats}")
            
            # Test world stats
            world_stats = DatabaseOptimizer.get_world_stats(db, cache)
            print(f"✅ World stats: {world_stats}")
            
            return True
    except Exception as e:
        print(f"❌ DatabaseOptimizer error: {e}")
        return False

def test_routes():
    """Test if routes are accessible"""
    print("Testing routes...")
    try:
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Home page accessible")
            else:
                print(f"❌ Home page error: {response.status_code}")
                return False
            
            # Test auth page
            response = client.get('/auth')
            if response.status_code == 200:
                print("✅ Auth page accessible")
            else:
                print(f"❌ Auth page error: {response.status_code}")
                return False
            
            return True
    except Exception as e:
        print(f"❌ Routes error: {e}")
        return False

def test_configuration():
    """Test configuration settings"""
    print("Testing configuration...")
    try:
        # Test secret key
        if app.config.get('SECRET_KEY'):
            print("✅ Secret key configured")
        else:
            print("❌ Secret key not configured")
            return False
        
        # Test database URI
        if app.config.get('SQLALCHEMY_DATABASE_URI'):
            print("✅ Database URI configured")
        else:
            print("❌ Database URI not configured")
            return False
        
        # Test cache configuration
        try:
            cache.set('test', 'value', timeout=10)
            result = cache.get('test')
            if result == 'value':
                print("✅ Cache configured and working")
            else:
                print("❌ Cache not working properly")
                return False
        except Exception as e:
            print(f"❌ Cache error: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting application tests...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_database_connection,
        test_database_optimizer,
        test_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 30)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
