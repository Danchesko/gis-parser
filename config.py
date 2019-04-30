import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SELENIUM_BOOST_OPTIONS=False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProductionConfig(Config):
    SELENIUM_BOOST_OPTIONS=True

class TestingConfig(Config):
    TESTING = True