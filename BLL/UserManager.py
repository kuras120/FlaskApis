from ORM.DbConfig import DbConfig
from ORM.User import User
import hashlib
import uuid


class UserManager:
    def __init__(self):
        self.__session = DbConfig().get_session()

    def add_user(self, login, password):
        if not self.__session.query(User).filter(User.login == login).one():
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password + salt).hexdigest()
            new_user = User(login=login, hashed_password=hashed_password, salt=salt)
            self.__session.add(new_user)
            self.__session.commit()

    def check_user(self, login, password):
        user = self.__session.query(User).filter(User.login == login).one()
        hash_password = hashlib.sha512(password + user.salt).hexdigest()
        if user.hashed_password == hash_password:
            return True
        else:
            return False
