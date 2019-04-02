import logging

from BLL.UserManager import UserManager
from ORM.DbConfig import init_db


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


def init_config():
    init_loggers()
    logging.getLogger('logger').info('Loggers initialized.')
    init_db()
    logging.getLogger('logger').info('Db initialized.')

    try:
        UserManager.create_user('admin@gmail.com', 'admin1')
        UserManager.create_user('user@gmail.com', 'user1')
        print('Test accounts added.')
    except Exception as e:
        print('Error: ' + e.__str__())
        print('Test accounts already added.')


