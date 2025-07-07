import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'production': DevelopmentConfig,
    'default': DevelopmentConfig
}
