from itertools import product
from flask import request, make_response as response, jsonify
from marshmallow import ValidationError

from config import db
from config.base import BaseView
from config.utils import get_user
from config.permissions import authorized_only

from cart.models import CartItem
from cart.serializers import CartItemSchema
from products.models import Product


class CartItemAPIView(BaseView):

    decorators = [authorized_only]

    def get(self):
        schema = CartItemSchema(many=True)
        try:
            user = get_user()
            if user is not None:
                cart_items = db.Session.query(CartItem).filter(
                    CartItem.customer == user.id).all()
                data = schema.dumps(cart_items)
                return response(jsonify(data), 200)
            return response("", 401)
        except:
            return response("", 500)

    def post(self):
        schema = CartItemSchema()
        try:
            data = schema.load(request.json)
            assert request.json is not None
            product_id = request.json["product_id"]
            product = db.Session.query(Product).filter(Product.id == product_id).first()
            user = get_user()
            if user is not None:
                query = db.Session.query(CartItem).filter(CartItem.customer == user.id, CartItem.product == product)
                if query.first() is not None:
                    if data["quantity"] == 0:
                        query.delete()
                    else:
                        query.first().quantity = data["quantity"]
                    db.Session.commit()
                    return response("", 200)
                cart_item = CartItem(customer=user.id, product=product, quantity=data["quantity"])
                db.Session.add(cart_item)
                db.Session.commit()
                return response("", 200)
            return response("", 401)
        except (ValidationError, KeyError, AssertionError):
            return response("", 400)
        except: # catch database errors
            return response("", 500)
