import datetime

from sqlalchemy import Column, Boolean, String, Date

from config import db


class Staff(db.Base):
    __tablename__ = 'staff'

    username = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    joined = Column(Date, default=datetime.date.today())

    def __repr__(self):
        return "<Product (username=%s, name=%s)>" % (self.username, self.name)
