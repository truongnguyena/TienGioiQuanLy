import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_caching import Cache
from config import config

# Configure logging based on environment
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[config_name])

# Apply proxy fix for production
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure caching
cache = Cache(app)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'  # type: ignore

with app.app_context():
    import models
    import routes
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
