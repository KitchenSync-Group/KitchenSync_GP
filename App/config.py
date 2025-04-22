import os

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_key')
    RECIPE_API_KEY = os.environ.get('RECIPE_API_KEY', '')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}