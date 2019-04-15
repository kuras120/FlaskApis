import logging

from ORM import db
from ORM.Data import Data

from Utilities.CustomExceptions import UserException, DatabaseException


class DataDAO:
    @staticmethod
    def create(file_name, user):
        try:
            if not db.session.query(Data).filter(Data.file_name == file_name, Data.user_id == user.id).first():
                new_data = Data(file_name=file_name, user_name=user.login)
                user.data.append(new_data)
                db.session.merge(user)
                db.session.commit()
                return new_data
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

        msg = 'File with this name already exists.'
        logging.getLogger('logger').warning(msg)
        raise UserException(msg)

    @staticmethod
    def read(file_name, user):
        try:
            data = db.session.query(Data).filter(Data.file_name == file_name, Data.user_id == user.id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
        if data:
            return data
        else:
            logging.getLogger('logger').warning('File not found.')
            raise UserException()

    @staticmethod
    def update(data):
        if data:
            try:
                db.session.merge(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Update data error. Data not found.')
            raise UserException('Data doesn\'t exists.')

    @staticmethod
    def delete(data):
        if data:
            try:
                db.session.delete(data)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logging.getLogger('error_logger').exception(e)
                raise DatabaseException()
        else:
            logging.getLogger('logger').warning('Delete data error. Data not found.')
            raise UserException('Data doesn\'t exists.')

    @staticmethod
    def delete_all():
        try:
            return db.session.query(Data).delete()
        except Exception as e:
            db.session.rollback()
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get(data_id):
        try:
            return db.session.query(Data).filter(Data.id == data_id).first()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()

    @staticmethod
    def get_all(user_id):
        try:
            return db.session.query(Data).filter(Data.user_id == user_id).all()
        except Exception as e:
            logging.getLogger('error_logger').exception(e)
            raise DatabaseException()
