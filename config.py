import os

class Config:
""" Main configuration"""
    TESTING=False
    DEBUG=False

class DevelopmentConfig(Config):
""" The configuration for environment configuration"""
    TESTING = True    
    DEBUG = True
    

class TestConfig(Config):   
""" The configuration for testing"""
    TESTING = True
    DEBUG=True
