import os
import boto3
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()
ssm = boto3.client('ssm', region_name=os.getenv('REGION'))


class BaseConfig:
    # def __init__(self):
    #     self.__params

    @staticmethod
    # @lru_cache()
    def _get_params():
        # if not self.__params:
        params = ssm.get_parameter(Name=f'{os.getenv("PREFIX")}-aws-upskill-db-creds-{os.getenv("FLASK_ENV")}',
                                          WithDecryption=True)['Parameter']['Value'].split(',')
        # print(self.__params)
        return params

    # @property
    # def database_url(self):
    #     return self._get_params()[f'paran-db-connection-{env_jakis_tam}']


class DevConfig(BaseConfig):
    """
      Development configurations
    """
    _env_key = 'dev'
    rds_endpoint = 'localhost'
    port = 5432


class ProdConfig(BaseConfig):
    """
      Production configurations
    """


def get_config():
    app_env = {"dev": DevConfig,
               "prod": ProdConfig}
    return app_env[os.getenv('FLASK_ENV')]

