import os

import boto3
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    PORT = os.getenv("PORT")
    HOST = os.getenv("HOST")
    AWS_REGION = os.getenv("AWS_REGION")
    TABLE_NAME = os.getenv("TABLE_NAME")


class DevelopmentConfig(BaseConfig):
    """
    Development configurations
    """
    CLIENT = boto3.client('dynamodb', region_name=f'{BaseConfig.AWS_REGION}')
    RESOURCE = boto3.resource('dynamodb', region_name=f'{BaseConfig.AWS_REGION}')


class ProductionConfig(BaseConfig):
    """
    Production configurations
    """
    FLASK_DEBUG = 1
    CLIENT = boto3.client('dynamodb', endpoint_url=f"http://{BaseConfig.HOST}:{BaseConfig.PORT}")
    RESOURCE = boto3.resource('dynamodb', endpoint_url=f"http://{BaseConfig.HOST}:{BaseConfig.PORT}")


# class DockerConfig(BaseConfig):
#     """
#     Production configurations
#     """
#     HOST = 'database'
#     FLASK_DEBUG = True
#     DEBUG = True


def get_config():
    app_env = {"dev": DevelopmentConfig,
               "prod": ProductionConfig}

    print(f"FLASK_ENV: {os.getenv('FLASK_ENV')} !!!")
    return app_env[os.getenv('FLASK_ENV')]