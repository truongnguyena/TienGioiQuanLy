import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tu_tien.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Security settings
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # Production-specific settings
    if os.environ.get('DATABASE_URL', '').startswith('postgresql'):
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_recycle': 300,
            'pool_pre_ping': True,
            'pool_size': 10,
            'max_overflow': 20
        }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
