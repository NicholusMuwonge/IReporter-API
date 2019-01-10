"""
App configurations
"""


class Config:
    """
    This is the parent configurations to be inherited from
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "apple123"


class DevelopmentConfig(Config):
    """
    The configuration for the development environment
    """
    DEBUG = True
    TESTING = True
    ENV = 'development'
    SECRET_KEY = 'apple123'


class TestingConfig(Config):
    """
    The configuration for testing
    """
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'apple123'
