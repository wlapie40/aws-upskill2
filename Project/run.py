import logging as logger
import os
import time

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import (database_exists,
                              create_database,)

from Project.aws.cloud_watch.logs.log_events import CloudWatchLogger
from Project.aws.entities.filters import (datetimeformat,
                                          file_type,)
from Project.aws.gateways.parameter_store import _read_parameters_store
from Project.config import DevelopmentConfig
from Project.user.models import db

#  todo move to separate class obj

# logger.basicConfig(filename='project/logs/app_logs',
#                             filemode='a',
#                             format=f'%(levelname)s:%(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logger.INFO)


class ParameterStore:
    def __init__(self):
        self._parameters = {'prod': 'sfigiel-prod-db-cred',
                            'dev': 'sfigiel-dev-db-cred',
                            'docker': 'sfigiel-docker-db-cred'}

    def add_param(self, param_name, param_value):
        self._parameters[param_name] = param_value


def _cloud_watch_monitoring():
    log = CloudWatchLogger()
    #  todo check if ParameterStore exists

    if not log.describe_log_groups()['logGroups']:
        log.create_log_group()
        log.create_log_stream()
        log.put_log_events(message='init logs')  # in case of getting new sequenceToken
    else:
        log.put_log_events(message='start app...')
    return log


def create_app():
    cur_env = str(os.environ['FLASK_ENV'])

    param = ParameterStore()
    try:
        param_store_name = param._parameters[cur_env]
    except:
        raise KeyError(f'FLASK_ENV value has not been set up.')

    param_store = _read_parameters_store(param_store_name, True)
    config = DevelopmentConfig(*param_store)

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'the random string'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    logger.info(f'DATABASE_CONNECTION_URI: {config.DATABASE_CONNECTION_URI}')

    cw_log = _cloud_watch_monitoring()
    cw_log.put_log_events(message=f'DATABASE_CONNECTION_URI: {config.DATABASE_CONNECTION_URI}')

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    logger.info(f'CREATING DB ENGINE ...')
    cw_log.put_log_events(message=f'CREATING DB ENGINE ...')

    time.sleep(3)  # let's give a bit more time our DB to wake up :)
    engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    logger.info(f'DATABASE_ENGINE: {database_exists(engine.url)}')
    cw_log.put_log_events(message=f'DATABASE_ENGINE: {database_exists(engine.url)}')

    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
        api = Api(flask_app)
        Bootstrap(flask_app)

        login_manager = LoginManager()
        login_manager.init_app(flask_app)
        login_manager.login_view = 'login'

        flask_app.jinja_env.filters['datetimeformat'] = datetimeformat
        flask_app.jinja_env.filters['file_type'] = file_type

    return flask_app, api, login_manager, cur_env, cw_log
