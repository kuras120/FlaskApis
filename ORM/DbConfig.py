import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DbConfig:
    def __init__(self):
        self.__logger = logging.getLogger('logger')
        self.__engine = create_engine('sqlite:///Controllers/static/DB/simple.db')
        Base.metadata.create_all(self.__engine)
        self.__logger.info("Db initialized.")
        self.__session = None

    def get_engine(self):
        return self.__engine

    def get_session(self):
        if not self.__session:
            try:
                Base.metadata.bind = self.__engine
                temp = sessionmaker(bind=self.__engine)
                self.__session = temp()
            except Exception as error:
                raise Exception(error)
        return self.__session
