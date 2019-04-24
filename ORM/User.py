import secrets
import hashlib
from datetime import datetime

from ORM import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime


class User(db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    home_catalog = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False)
    last_login = Column(DateTime, nullable=True)
    files = relationship("File", cascade="all, delete-orphan")
    history = relationship("History", cascade="all, delete-orphan")

    def __init__(self, login, password):
        self.login = login
        self.salt = secrets.token_hex(8)
        self.hashed_password = hashlib.sha3_512(password.encode("utf-8") + self.salt.encode("utf-8")).hexdigest()
        self.home_catalog = hashlib.sha3_256(login.__str__().encode('utf-8')).hexdigest()
        self.created_on = datetime.now().replace(microsecond=0)
        self.last_login = datetime.now().replace(microsecond=0)

    def __repr__(self):
        return '<User %s>' % self.login
