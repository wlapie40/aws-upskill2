import os

from dotenv import load_dotenv

from common.aws.gateways.parameter_store import read_parameters_store

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name == 'test':
            self.__name = 'TEST'
        elif name == 'test1234':
            self.__name = 'TEST1234'
        else:
            self.__name = 'qwerty'


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    DB_URI = f'sqlite:///' + os.path.join(basedir, os.getenv('LOCAL_DB_NAME'))
    FLASK_DEBUG = 1
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    DB_URI = read_parameters_store(param_name=f'{os.getenv("PARAMETER_STORE")}', with_decryption=True)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_DEBUG = 0


class DockerConfig(BaseConfig):
    """
    Production configurations
    """
    host = 'database'
    FLASK_DEBUG = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


def get_config():
    app_env = {"dev": DevelopmentConfig,
               "prod": ProductionConfig,
               "docker": DockerConfig}

    return app_env[os.getenv('FLASK_ENV')]
