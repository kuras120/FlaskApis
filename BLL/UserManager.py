from ORM.User import User
import hashlib
import uuid


class UserManager:
    def __init__(self, session):
        self.__session = session

    def add_user(self, login, password):
        new_user = None
        if not self.__session.query(User).filter(User.login == login).first():
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password.encode("utf-8") + salt.encode("utf-8")).hexdigest()
            new_user = User(login=login, hashed_password=hashed_password, salt=salt)
            self.__session.add(new_user)
            self.__session.commit()
        return new_user

    def check_user(self, login, password):
        user = self.__session.query(User).filter(User.login == login).first()
        hash_password = hashlib.sha512(password.encode('utf-8') + user.salt).hexdigest()
        if user.hashed_password == hash_password:
            return user
        else:
            return None
