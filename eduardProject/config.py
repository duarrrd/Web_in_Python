import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if os.getenv('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class ProdConfig(Config):
    pass  # No need to set SQLALCHEMY_DATABASE_URI here if it's the same as Config

class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "tests-db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config = {
    'DEV': DevConfig,
    'PROD': ProdConfig,
    'DEF': DevConfig,
    'TEST': TestConfig
}
