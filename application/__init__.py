from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ, path
from dotenv import load_dotenv
import os
from werkzeug.utils import import_string
from config import config_by_name

from flask_login import LoginManager


# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()


def page_not_found(e):
    return render_template('404.html'), 404

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=True)
    config_name = 'dev'
    app.config.from_object(config_by_name[config_name])

    
    
    
    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    app.register_error_handler(404, page_not_found)

    with app.app_context():
        # Include our Routes
        from .drivers import routes
        from .home import routes
        from .auth import routes
        from .vehicles import routes
        from .trackers import routes
        from .users import routes
        from .maintenance import routes
        app.register_blueprint(auth.routes.auth_bp)
        app.register_blueprint(drivers.routes.drivers_bp)
        app.register_blueprint(home.routes.home_bp)    
        app.register_blueprint(vehicles.routes.vehicles_bp)    
        app.register_blueprint(users.routes.users_bp)    
        app.register_blueprint(trackers.routes.trackers_bp)    
        app.register_blueprint(maintenance.routes.maintenance_bp)
        
        return app