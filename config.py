from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """Set Flask config variables."""
    
    FLASK_ENV = 'development'
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_RUN_PORT = environ.get('FLASK_RUN_PORT')
    

    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False




class ProdConfig(Config):
    ENV = 'production'
    FLASK_DEBUG = 0

    TESTING = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')
    
    


class DevConfig(Config):
    ENV = 'development'
    FLASK_DEBUG = 1
    TESTING = True
    
    DATABASE_URI = environ.get('DEV_DATABASE_URI')
    

    

