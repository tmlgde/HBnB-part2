import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

config = {
        'development': DevelopmentConfig,
        'production': DevelopmentConfig,
        'default': DevelopmentConfig
        }
