from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# Globally accessible libraries
db = SQLAlchemy()



def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    

    with app.app_context():
        # Include our Routes
        from .drivers import routes
        from .home import routes
        app.register_blueprint(drivers.routes.drivers_bp)
        app.register_blueprint(home.routes.home_bp)
    

        return app