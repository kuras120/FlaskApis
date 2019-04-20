from ORM import db
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Data(db.Model):
    __tablename__ = "Data"
    id = Column(Integer, primary_key=True)
    file_name = Column(String, nullable=False)
    added_on = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"))

    def __init__(self, file_name):
        self.file_name = file_name
        self.added_on = datetime.now().replace(microsecond=0)

    def __repr__(self):
        return '<File %s>' % self.file_name
