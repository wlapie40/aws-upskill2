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
from common.config.config import get_config
from common.logger import *
from common.user.models import db

CUR_ENV = str(os.environ['FLASK_ENV'])


def create_app():
    logger.info(f'cur_env: {CUR_ENV}')
    config = get_config()

    logger.info(f'dict config: {config.__dict__}')

    flask_app = Flask(__name__)
    flask_app.secret_key = config.SECRET_KEY

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
    logger.info(f'config.DB_URI: {config.DB_URI}')

    logger.info(f'SQLALCHEMY_DATABASE_URI: {config.DB_URI}')

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

    return flask_app, api, login_manager, CUR_ENV, logger
