from sqlalchemy import Column, Integer, String

from ORM.DbConfig import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
