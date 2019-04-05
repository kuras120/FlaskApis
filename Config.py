import os
import logging

from ORM import db
from ORM.User import User
from BLL.UserManager import UserManager

from HomeController import home_controller
from UserController import user_controller


def bind_blueprints(app):
    app.register_blueprint(home_controller, url_prefix='/')
    app.register_blueprint(user_controller, url_prefix='/account')


def init_db(app):
    if not os.path.isdir('static/DB'):
        os.makedirs('static/DB')
        print('DB folder created.')

    db.app = app
    db.init_app(app)
    db.create_all()


def init_loggers():
    # -- LOGGERS -- #
    logger = logging.getLogger('logger')
    error_logger = logging.getLogger('error_logger')

    logger.setLevel(logging.INFO)
    error_logger.setLevel(logging.DEBUG)

    if not os.path.isdir('Logs'):
        os.makedirs('Logs')
        print('Logs folder created.')

    fh = logging.FileHandler('Logs/info.log')
    fher = logging.FileHandler('Logs/error.log')
    ch = logging.StreamHandler()

    fh.setLevel(logging.INFO)
    fher.setLevel(logging.DEBUG)
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    fher.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    error_logger.addHandler(fher)
    error_logger.addHandler(ch)


def init_debug():
    try:
        db.session.query(User).delete()

        # Add users
        UserManager.create_user('admin@gmail.com', 'admin1')
        UserManager.create_user('user@gmail.com', 'user1')

        # Update user
        usr = UserManager.get_user(2)
        usr.login = 'eladminos@gmail.com'
        usr.hashed_password = 'eladminos1'
        UserManager.update_user(usr)

    except Exception as e:
        print('Error: ' + e.__str__())





