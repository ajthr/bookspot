import datetime

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.schema import Sequence

from config import db


class Product(db.Base):
    __tablename__ = 'product'

    id = Column(Integer, Sequence('product_id', start=10000,
                increment=1), primary_key=True, unique=True)
    isbn = Column(String, unique=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    msrp = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    popularity = Column(Integer, default=0)
    published = Column(Date, default=datetime.date.today())
    copies = Column(Integer, nullable=False)
    created = Column(Date, default=datetime.date.today())

    def __repr__(self):
        return "<Product (id=%s, title=%s)>" % (self.id, self.title)
