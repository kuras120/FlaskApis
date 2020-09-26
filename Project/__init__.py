import os
import redis
import logging
from flask import Flask

from rq import Connection, Queue
from Project.Server.ORM import db
from Project.Config import init_loggers, init_debug
from Project.Server.Controllers.HomeController import home_controller
from Project.Server.Controllers.UserController import user_controller
from Project.Server.Controllers.FileController import file_controller


def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder='Client/templates',
        static_folder='Client/static'
    )

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    if not app_settings:
        app_settings = 'Project.Config.DevelopmentGlobalConfig'
    app.config.from_object(app_settings)

    init_loggers()
    logging.getLogger('logger').info('Loggers initialized.')

    db.app = app
    db.init_app(app)
    db.create_all()
    logging.getLogger('logger').info('Db initialized.')

    if os.getenv('FLASK_ENV') == 'development':
        init_debug(app)
        with Connection(redis.from_url(app.config['REDIS_URL'])):
            r = redis.Redis()
            r.flushall()
        logging.getLogger('logger').info('Debug mode on')

    # register blueprints
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')
    app.register_blueprint(file_controller, url_prefix='/account')

    # shell context for flask cli
    app.shell_context_processor({'app': app})

    return app
