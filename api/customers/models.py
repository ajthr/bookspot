import datetime

from sqlalchemy import Column, Integer, Boolean, String, Date, ForeignKey

from config import db

class Customer(db.Base):
    __tablename__ = 'customer'

    id = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    joined = Column(Date, default=datetime.date.today())

    def __repr__(self):
        return "<Customer (id=%s, email=%s)>" % (self.id, self.email)

class Address(db.Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    customer = Column(String, ForeignKey('customer.id', ondelete="CASCADE"))
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    locality = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    pincode = Column(String, nullable=False)
    office = Column(Boolean, default=False)
    default = Column(Boolean, default=False)

    def __repr__(self):
        return "<Address (id=%s, name=%s)>" % (self.id, self.name)
