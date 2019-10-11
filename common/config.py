import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_uri ='sqlite:///' + os.path.join(basedir, self.db_name)


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    host = 'localhost'  # in case of using docker
    FLASK_DEBUG = 1
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_DEBUG = 0


class DockerConfig(BaseConfig):
    """
    Production configurations
    """
    host = 'database'
    FLASK_DEBUG = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
