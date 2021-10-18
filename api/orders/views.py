import uuid
import stripe
from flask import request, make_response as response, jsonify
from marshmallow import ValidationError

from config import db, settings
from config.base import BaseView
from config.utils import get_user
from config.permissions import authorized_only

from orders.models import Order, OrderItem
from cart.models import CartItem
from products.models import Product
from customers.models import Address
from orders.serializers import OrderSchema

stripe.api_key = settings.STRIPE_API_KEY


class OrdersAPIView(BaseView):

    decorators = [authorized_only]

    def get(self):
        schema = OrderSchema(many=True)
        try:
            user = get_user()
            orders = db.Session.query(Order).filter(
                Order.customer == user.id).all()
            data = schema.dump(orders)
            return response(jsonify(data), 200)
        except:
            return response("", 401)


class OrderAPIView(BaseView):

    decorators = [authorized_only]

    def get(self, id):
        schema = OrderSchema()
        try:
            user = get_user()
            order = db.Session.query(Order).filter(Order.id == id).first()
            if order.customer == user.id:
                if order is not None:
                    data = schema.dump(order)
                    return response(jsonify(data), 200)
                return response("", 404)
            return response("", 401)
        except:  # catch database errors
            return response("", 500)

    def patch(self, id):
        schema = OrderSchema()
        try:
            data = schema.loads(request.json)
            user = get_user()
            order = db.Session.query(Order).filter(Order.id == id).first()
            if order.customer == user.id:
                if order is not None:
                    address = db.Session.query(Address).filter(
                        Address.id == id).first()
                    if address is not None:
                        order.address_id = data["address_id"]
                        db.Session.commit()
                        return response("", 200)
                    return response("", 400)
                return response("", 404)
        except ValidationError:
            return response("", 400)
        except:  # catch db exceptions
            return response("", 500)


class CreateOrderAPIView(BaseView):

    decorators = [authorized_only]

    def post(self):
        schema = OrderSchema()
        try:
            data = schema.loads(request.json)
            user = get_user()

            id = uuid.uuid4().hex
            exists = db.Session.query(Order).filter(Order.id == id).first()
            while exists is not None:
                id = uuid.uuid4().hex
                exists = db.Session.query(Order).filter(Order.id == id).first()
            data["customer"] = user.id
            data["amount"] = 0
            data["id"] = id
            order = Order(**data)
            db.Session.add(order)
            db.Session.flush()

            amount = 0
            cart_items = db.Session.query(CartItem).filter(
                CartItem.customer == user.id).all()
            if cart_items is not None:
                for item in cart_items:
                    product = db.Session.query(Product).filter(
                        Product.id == item.product_id).first()
                    if product is not None:
                        amount += (product.price * item.quantity)
                        order_item = OrderItem(
                            order_id=id, product=product.id, quantity=item.quantity)
                        db.Session.add(order_item)
                        db.Session.flush()

            order.amount = amount
            db.Session.commit()

            intent = stripe.PaymentIntent.create(
                amount=1099,
                currency='inr',
                payment_method_types=['card'],
                metadata={
                    "order_id": "order_id"
                }
            )
            return response(jsonify(client_secret=intent.client_secret), 200)
        except ValidationError:
            return response("", 400)


class ConfirmPaymentAPIView(BaseView):

    def post(self):
        event = None
        payload = request.data
        sig_header = request.headers['STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return response("", 400)

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = payment_intent["metadata"]["order_id"]
            order = db.Session.query(Order).filter(
                Order.id == order_id).first()
            if order is None:
                return response("", 404)
            order.payment_completed = True
            order.payment_intent = payment_intent["payment_intent"]
            db.Session.commit()
        return response("", 200)


class CancelOrderAPIView(BaseView):

    def post(self, id):
        try:
            order = db.Session.query(Order).filter(Order.id == id).first()
            if order is None:
                return response("", 404)
            stripe.Refund.create(
                amount=order.amount,
                payment_intent=order.payment_intent,
            )
            order.cancelled = True
            db.Session.commit()
            return response("", 200)
        except:
            return response("", 500)
