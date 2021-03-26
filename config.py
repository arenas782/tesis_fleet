import os


class Config():
    DEBUG = False
    TESTING = False    
    SECRET_KEY = 'secret_key'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SESSION_COOKIE_NAME = 'uneg_fleet_cookie_session'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:toor@localhost/tesis'
    FLASK_ENV = 'development'    
    ENV = 'development'
    FLASK_RUN_PORT = 5000
    UPLOAD_FOLDER = '/home/arenas/Escritorio/tesis/application/static/uploads'
    
    

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:Abc123..@localhost/tesis'
    FLASK_ENV = 'production'    
    ENV = 'production'    
    UPLOAD_FOLDER = '/home/arenas/Escritorio/tesis/application/static/uploads'
    
config_by_name = dict(
    dev=DevelopmentConfig,    
    prod=ProductionConfig    
)







