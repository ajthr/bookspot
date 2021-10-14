from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import Sequence

from config import db


class CartItem(db.Base):
    __tablename__ = "cart_item"

    id = Column(Integer, Sequence('cart_id', start=100,
                increment=1), primary_key=True, unique=True)
    customer = Column(String, ForeignKey('customer.id', ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey('product.id', ondelete="CASCADE"))
    quantity = Column(Integer, default=1)

    product = relationship("Product", foreign_keys=[product_id])

    def __repr__(self):
        return "<CartItem (product=%s, quantity=%s)>" % (self.product_id, self.quantity)
