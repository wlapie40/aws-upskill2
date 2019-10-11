import logging as logger
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import (database_exists,
                              create_database, )

from common.aws.entities.filters import (datetimeformat,
                                         file_type, )
from common.config import DevelopmentConfig
from common.user.models import db

#  todo move to separate class obj

logger.basicConfig(filename='app_logs',
                            filemode='a',
                            format=f'%(levelname)s:%(message)s',
                            datefmt='%H:%M:%S',
                            level=logger.INFO)

DB_NAME = {
    'prod': 'prod-db',
    'dev': 'dev-db',
    'docker': 'docker-db',
}


def create_app():
    cur_env = str(os.environ['FLASK_ENV'])
    print(f'cur_env: {cur_env} !!!')

    db_name = DB_NAME[cur_env]

    config = DevelopmentConfig(db_name)

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'the random string'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    logger.info(f'DATABASE_CONNECTION_URI: {config.db_uri}')

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    logger.info(f'CREATING DB ENGINE ...')

    engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(engine.url):
        create_database(engine.url)

    logger.info(f'DATABASE_ENGINE: {database_exists(engine.url)}')

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

    return flask_app, api, login_manager, cur_env
