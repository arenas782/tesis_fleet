from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ, path
from dotenv import load_dotenv
import os

from flask_login import LoginManager

# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)

    
    
    app.config.from_object('config.DevConfig')
    
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    

    with app.app_context():
        # Include our Routes
        from .drivers import routes
        from .home import routes
        from .auth import routes
        app.register_blueprint(auth.routes.auth_bp)
        app.register_blueprint(drivers.routes.drivers_bp)
        app.register_blueprint(home.routes.home_bp)    
        return app