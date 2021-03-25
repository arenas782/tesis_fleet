from os import environ, path
from dotenv import load_dotenv


class Config(object):
    DEBUG = False
    TESTING = False    


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:toor@localhost/tesis'
    FLASK_ENV = 'development'
    SECRET_KEY = 'secret_key'
    FLASK_RUN_PORT = 5000
    UPLOAD_FOLDER = '/home/arenas/Escritorio/tesis/application/static/uploads'


    SESSION_COOKIE_NAME = 'uneg_fleet_cookie_session'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False






