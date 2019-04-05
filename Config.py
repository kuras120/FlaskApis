import logging

from BLL.UserManager import UserManager
from ORM.DbConfig import db_session
from ORM.User import User


class Config:
    @staticmethod
    def init_loggers():
        # -- LOGGERS -- #
        logger = logging.getLogger('logger')
        error_logger = logging.getLogger('error_logger')

        logger.setLevel(logging.INFO)
        error_logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('Logs/info.log')
        fh.setLevel(logging.INFO)

        fher = logging.FileHandler('Logs/error.log')
        fher.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh.setFormatter(formatter)

        fher.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)

        error_logger.addHandler(fher)
        error_logger.addHandler(ch)

    @staticmethod
    def init_debug():
        try:
            db_session.query(User).delete()
        except Exception as e:
            print('Error: ' + e.__str__())
        try:
            # Create users
            UserManager.create_user('admin@gmail.com', 'admin1')
            UserManager.create_user('user@gmail.com', 'user1')
            print('Test accounts added.')

            # Update user admin
            usr = UserManager.get_user(2)
            usr.login = 'eladminos@gmail.com'
            usr.hashed_password = 'eladminos1'
            UserManager.update_user(usr)

        except Exception as e:
            print('Error: ' + e.__str__())


