import os

from dotenv import load_dotenv, find_dotenv
from common.logger import *
from common.aws.gateways.parameter_store import read_parameters_store

load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.urandom(12).hex()
    PARAMETER_STORE_REGION = os.getenv("PARAMETER_STORE_REGION")
    FLASK_ENV = os.getenv("FLASK_ENV")
    LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME", None)
    PARAMETER_STORE = os.getenv("PARAMETER_STORE_REGION")


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
                                   region_name=f'{os.getenv("PARAMETER_STORE_REGION")}',
                                   with_decryption=True)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DockerConfig(BaseConfig):
    """
    Production configurations
    """
    HOST = 'database'
    DB_URI = 'mysql://test:test123456@database/db_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


def get_config():
    app_env = {"dev": DevelopmentConfig,
               "prod": ProductionConfig,
               "docker": DockerConfig}
    logger.info(f'FLASK_ENV: {app_env[os.getenv("FLASK_ENV")]}')
    return app_env[os.getenv('FLASK_ENV')]
