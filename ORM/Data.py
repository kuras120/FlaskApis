from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ORM import db


class Data(db.Model):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("User")

    def __init__(self, file_name, file_path, user_id):
        self.file_name = file_name
        self.file_path = file_path
        self.added_on = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<File %s>' % self.file_name
