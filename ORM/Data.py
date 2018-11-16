from sqlalchemy import Column, Integer
from ORM.DbConfig import Base


class Data(Base):
    __tablename__ = "Data"

    id = Column(Integer, primary_key=True)
    key = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
