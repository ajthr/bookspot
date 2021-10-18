import datetime

from sqlalchemy import Column, Boolean, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from config import db


class Order(db.Base):
    __tablename__ = "order"

    id = Column(String, primary_key=True, unique=True)
    customer = Column(String, ForeignKey(
        'customer.id', ondelete="CASCADE"), nullable=False)
    address_id = Column(Integer, ForeignKey(
        'address.id', ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_completed = Column(Integer, default=False, nullable=False)
    payment_intent  = Column(String)
    completed = Column(Boolean, default=False, nullable=True)
    cancelled = Column(Boolean, default=False, nullable=True)

    address = relationship('Address', foreign_keys=[address_id])

    def __repr__(self):
        return "<Order (id=%s, amount=%s)>" % (self.id, self.amount)


class OrderItem(db.Base):
    __tablename__ = "order_item"

    order_id = Column(String, ForeignKey(
        'order.id', ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    product = relationship("Product", foreign_keys=[product_id])

    def __repr__(self):
        return "<OrderItem (order=%s, product=%s)>" % (self.order_id, self.product_id)
