import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SELENIUM_OPTIONS=False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG=False
    SELENIUM_OPTIONS=True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SELENIUM_OPTIONS=True


class TestingConfig(Config):
    TESTING = True