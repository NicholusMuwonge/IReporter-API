"""
App configurations
"""


class Config:
    """
    This is the parent configurations to be inherited from
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "nicksbro"


class DevelopmentConfig(Config):
    """
    The configuration for the development environment
    """
    DEBUG = True
    TESTING = True
    ENV = 'development'
    SECRET_KEY = 'nicksbro'


class TestingConfig(Config):
    """
    The configuration for testing
    """
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'nicksbro'
