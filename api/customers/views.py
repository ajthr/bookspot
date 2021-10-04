from flask import request, make_response as response, jsonify
from marshmallow import ValidationError

from google.oauth2 import id_token
from google.auth.transport import requests

from config import db, settings
from config.base import BaseView
from config.permissions import authorized_only
from config.utils import totp, send_mail, signin, get_instance

from customers.models import Customer, Address
from customers.serializers import CustomerSchema, AddressSchema


class CustomerApiView(BaseView):

    decorators = [authorized_only]

    def get(self):
        user = get_instance(Customer)
        if user is not None:
            schema = CustomerSchema()
            data = schema.dump(user)
            return response(jsonify(data), 200)
        return response("", 401)

    def patch(self):
        try:
            name = request.json['name']
            user = get_instance(Customer)
            if user is not None:
                user.name = name
                db.Session.commit()
                return response("", 200)
            return response("", 401)
        except (KeyError, TypeError):
            return response("", 400)


class EmailAPIView(BaseView):

    def post(self):
        try:
            email = request.json["email"]
            otp = totp.now()
            return send_mail(email, otp)
        except (KeyError, TypeError):
            return response("", 400)
        except:  # catch exceptions from totp.now()
            return response("", 500)


class EmailSigninAPIView(BaseView):

    def post(self):
        try:
            email = request.json["email"]
            otp = request.json["otp"]
            name = ''.join([i for i in email.split('@')[0] if not i.isdigit()])
            if totp.verify(otp):
                return signin(name, email)
            return response("", 400)
        except (KeyError, TypeError):
            return response("", 400)
        except:  # catch exceptions from totp.verify()
            return response("", 500)


class GoogleSigninAPIView(BaseView):

    def post(self):
        try:
            gtoken = request.json["token"]
            idinfo = id_token.verify_oauth2_token(
                gtoken, requests.Request(), settings.GOOGLE_CLIENT_ID)
            email = idinfo['email']
            name = idinfo["name"]
            return signin(name, email)
        except (KeyError, TypeError, ValueError):
            return response("", 400)


class LogoutAPIView(BaseView):

    decorators = [authorized_only]

    def post(self):
        try:
            resp = response("", 200)
            resp.delete_cookie("__USESSID_")
            return resp
        except:
            return response("", 401)


class AddressAPIView(BaseView):

    decorators = [authorized_only]

    def get(self):
        user = get_instance(Customer)
        if user is not None:
            addresses = db.Session.query(Address).filter(
                Address.customer == user.id).all()
            schema = AddressSchema(many=True)
            data = schema.dump(addresses)
            return response(jsonify(data), 200)
        return response("", 401)

    def post(self):
        schema = AddressSchema()
        try:
            user = get_instance(Customer)
            if user is not None:
                schema.load(request.json)
                address = Address(customer=user.id,
                                  name=request.json["name"],
                                  address=request.json["address"],
                                  locality=request.json["locality"],
                                  city=request.json["city"],
                                  state=request.json["state"],
                                  mobile=request.json["mobile"],
                                  pincode=request.json["pincode"],
                                  office=request.json["office"],
                                  default=request.json["default"]
                                  )
                db.Session.add(address)
                db.Session.commit()
                return response("", 200)
        except ValidationError:
            return response("", 400)
        except:
            return response("", 500)

    def patch(self):
        schema = AddressSchema()
        try:
            user = get_instance(Customer)
            if user is not None:
                schema.load(request.json)
                assert 'id' in request.json
                db.Session.query(Address).filter(
                    Address.id == request.json["id"]).update(request.json)
                db.Session.commit()
                return response("", 200)
            return response("", 200)
        except (ValidationError, AssertionError):
            return response("", 400)
        except: # catch db exceptions
            return response("", 500)
