"""
Database optimization utilities
"""
from sqlalchemy import func, desc, text
from functools import wraps
import time

def cache_query(cache, timeout=300):
    """Decorator to cache database queries"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
            return result
        return wrapper
    return decorator

class DatabaseOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def get_user_stats(db, cache):
        """Get user statistics with caching"""
        from models import User
        
        cache_key = "user_stats"
        result = cache.get(cache_key)
        if result is None:
            result = {
                'total_users': User.query.count(),
                'active_users': User.query.filter(User.last_cultivation > func.datetime('now', '-7 days')).count(),
                'new_users_today': User.query.filter(func.date(User.created_at) == func.date('now')).count()
            }
            cache.set(cache_key, result, timeout=300)
        return result
    
    @staticmethod
    def get_guild_stats(db, cache):
        """Get guild statistics with caching"""
        from models import Guild, User
        
        cache_key = "guild_stats"
        result = cache.get(cache_key)
        if result is None:
            result = {
                'total_guilds': Guild.query.count(),
                'active_guilds': Guild.query.filter(Guild.recruitment_open == True).count(),
                'top_guilds': db.session.query(
                    Guild.name, 
                    Guild.level, 
                    func.count(User.id).label('member_count')
                ).join(User, Guild.id == User.guild_id).group_by(Guild.id).order_by(desc('member_count')).limit(5).all()
            }
            cache.set(cache_key, result, timeout=600)
        return result
    
    @staticmethod
    def get_world_stats(db, cache):
        """Get world statistics with caching"""
        from models import World
        
        cache_key = "world_stats"
        result = cache.get(cache_key)
        if result is None:
            result = {
                'total_worlds': World.query.count(),
                'contested_worlds': World.query.filter(World.is_contested == True).count(),
                'high_level_worlds': World.query.filter(World.world_level >= 5).count()
            }
            cache.set(cache_key, result, timeout=300)
        return result
    
    @staticmethod
    def get_recent_achievements(db, cache, limit=10):
        """Get recent achievements with caching"""
        from models import Achievement
        
        cache_key = f"recent_achievements_{limit}"
        result = cache.get(cache_key)
        if result is None:
            result = Achievement.query.order_by(desc(Achievement.earned_at)).limit(limit).all()
            cache.set(cache_key, result, timeout=180)
        return result
    
    @staticmethod
    def optimize_user_queries(db):
        """Add database indexes for better performance"""
        try:
            # Add indexes for commonly queried columns
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_user_username ON user(username)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_user_guild_id ON user(guild_id)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_user_created_at ON user(created_at)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_user_cultivation_level ON user(cultivation_level)'))
            
            # Add indexes for World table
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_world_owner_id ON world(owner_id)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_world_world_level ON world(world_level)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_world_is_contested ON world(is_contested)'))
            
            # Add indexes for Guild table
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_guild_leader_id ON guild(leader_id)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_guild_recruitment_open ON guild(recruitment_open)'))
            
            # Add indexes for Expedition table
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_expedition_status ON expedition(status)'))
            db.engine.execute(text('CREATE INDEX IF NOT EXISTS idx_expedition_organizer_guild_id ON expedition(organizer_guild_id)'))
            
            print("Database indexes created successfully!")
            return True
        except Exception as e:
            print(f"Error creating indexes: {e}")
            return False
    
    @staticmethod
    def clear_cache(cache):
        """Clear all cached queries"""
        cache.clear()
        print("Cache cleared successfully!")

# Performance monitoring
def monitor_query_performance(func):
    """Decorator to monitor query performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        query_time = end_time - start_time
        if query_time > 1.0:  # Log slow queries
            print(f"Slow query detected: {func.__name__} took {query_time:.2f} seconds")
        
        return result
    return wrapper
