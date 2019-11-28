import os

from dotenv import load_dotenv, find_dotenv

from common.aws.gateways.parameter_store import read_parameters_store

load_dotenv(find_dotenv())

print(f'FLASK_ENV: {os.getenv("FLASK_ENV")}')
print(f'LOCAL_DB_NAME: {os.getenv("LOCAL_DB_NAME")}')
print(f'PARAMETER_STORE: {os.getenv("PARAMETER_STORE")}')

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.urandom(12).hex()

    def __init__(self, name):
        self.name = name
        self.secret_ket = os.urandom(12).hex()

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
    DB_URI = f'sqlite:///' + os.path.join(basedir,
                                          f"{os.getenv('LOCAL_DB_NAME') if os.getenv('LOCAL_DB_NAME') else None}")

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(BaseConfig):
    """sfigiel-aws-upskill-db-creds-prod
    Production configurations
    """
    DB_URI = read_parameters_store(param_name=f'{os.getenv("PARAMETER_STORE")}',
                                   with_decryption=True)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DockerConfig(BaseConfig):
    """
    Production configurations
    """
    host = 'database'
    DB_URI = 'mysql://test:test123456@database/db_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


def get_config():
    app_env = {"dev": DevelopmentConfig,
               "prod": ProductionConfig,
               "docker": DockerConfig}
    print(f'app_env: {app_env[os.getenv("FLASK_ENV")]}')
    return app_env[os.getenv('FLASK_ENV')]
