import os

basedir = os.path.abspath(os.path.dirname(__file__))
dbname = 'microblog.db'
dbscheme = 'sqlite:///'


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my customed key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              dbscheme + os.path.join(basedir, dbname) + '?check_same_thread=False'
    HOST = '192.168.0.127'
    PORT = 5001
    DEBUG = True


class ReleaseConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              dbscheme + os.path.join(basedir, dbname)
    HOST = '192.168.0.127'
    PORT = 5001
