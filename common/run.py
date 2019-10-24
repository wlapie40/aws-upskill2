import logging as logger
import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_restful import Api

from common.aws.entities.filters import (datetimeformat,
                                         file_type, )
from common.user.models import DynamoDB
from config.config import get_config

logger.basicConfig(filename='app_logs',
                            filemode='a',
                            format=f'%(levelname)s:%(message)s',
                            datefmt='%H:%M:%S',
                            level=logger.INFO)


def create_app():
    cur_env = os.getenv("FLASK_ENV")
    config = get_config()

    db = DynamoDB(table_name=config.TABLE_NAME, client=config.CLIENT, region=config.AWS_REGION,
                  resource=config.RESOURCE)
    db.create_db()

    flask_app = Flask(__name__)
    flask_app.config['SECRET_KEY'] = 'the random string'

    with flask_app.app_context():
        api = Api(flask_app)
        Bootstrap(flask_app)

        login_manager = LoginManager()
        login_manager.init_app(flask_app)
        login_manager.login_view = 'login'

        flask_app.jinja_env.filters['datetimeformat'] = datetimeformat
        flask_app.jinja_env.filters['file_type'] = file_type
    return flask_app, api, cur_env, db, login_manager
