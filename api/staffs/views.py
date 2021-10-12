import jwt
import bcrypt
from flask import request, make_response as response, jsonify
from marshmallow import ValidationError

from config import settings, db
from config.base import BaseView
from config.utils import get_staff
from config.permissions import admin_only, staff_only

from staffs.models import Staff
from products.models import Product
from staffs.serializers import StaffSchema
from products.serializers import ProductSchema


class CreateStaffAPIView(BaseView):

    decorators = [admin_only]

    def post(self):
        schema = StaffSchema()
        try:
            data = schema.load(request.json)
            data["password"] = bcrypt.hashpw(
                data["password"], bcrypt.gensalt())
            exists = db.Session.query(Staff).filter(
                Staff.username == data["username"]).first()
            if exists is not None:
                return response("", 409)
            staff = Staff(**data)
            db.Session.add(staff)
            db.Session.commit()
            return response("", 200)
        except ValidationError:
            return response("", 400)
        except:  # catch database errors
            return response("", 500)


class StaffLoginAPIView(BaseView):

    def post(self):
        schema = StaffSchema()
        try:
            data = schema.load(request.json)
            staff = db.Session.query(Staff).filter(
                Staff.username == data["username"]).first()
            if staff is not None:
                if bcrypt.checkpw(data["password"], staff.password):
                    token = jwt.encode(
                        {"username": staff.username}, settings.SECRET_KEY, algorithm="HS256")
                    resp = response("", 200)
                    resp.set_cookie("__STSSID_", token, httponly=True,
                                    secure=True, samesite='strict')
                    return resp
                return response("", 403)
            return response("", 401)
        except ValidationError:
            return response("", 400)
        except:  # catch database errors
            return response("", 500)


class StaffAPIView(BaseView):

    decorators = [staff_only]

    def get(self):
        schema = StaffSchema()
        staff = get_staff()
        if staff is not None:
            data = schema.dump(staff)
            data.pop('password')
            return response(jsonify(data), 200)
        return response(401)

    def patch(self):
        try:
            assert request.json is not None
            name = request.json["name"]
            staff = get_staff()
            if staff is not None:
                staff.name = name
                db.Session.commit()
                return response("", 200)
            return response("", 401)
        except (KeyError, AssertionError):
            return response("", 400)
        except:  # catch database error
            return response("", 500)


class StaffLogoutAPIView(BaseView):

    decorators = [staff_only]

    def post(self):
        try:
            resp = response("", 200)
            resp.delete_cookie("__STSSID_")
            return resp
        except:
            return response("", 401)


class StaffChangePasswordAPIView(BaseView):

    decorators = [staff_only]

    def post(self):
        try:
            assert request.json is not None
            password = request.json["password"]
            new_password = request.json["new_password"]
            staff = get_staff()
            if staff is not None:
                if bcrypt.checkpw(password, staff.password):
                    staff.password = bcrypt.hashpw(
                        new_password, bcrypt.gensalt())
                    db.Session.commit()
                    return response("", 200)
                return response("", 403)
            return response("", 401)
        except (KeyError, AssertionError):
            return response("", 400)
        except:  # catch database error
            return response("", 500)


class StaffResetPasswordAPIView(BaseView):

    decorators = [admin_only]

    def post(self):
        try:
            assert request.json is not None
            username = request.json["username"]
            password = request.json["password"]
            staff = db.Session.query(Staff).filter(
                Staff.username == username).first()
            if staff is not None:
                staff.password = bcrypt.hashpw(password, bcrypt.gensalt())
                db.Session.commit()
                return response("", 200)
            return response("", 401)
        except (KeyError, AssertionError):
            return response("", 400)
        except:  # catch database error
            return response("", 500)


class ManageProductsAPIView(BaseView):

    decorators = [staff_only]

    def post(self):
        schema = ProductSchema()
        try:
            data = schema.load(request.json)
            product = Product(**data)
            db.Session.add(product)
            db.Session.commit()
            return response("", 200)
        except ValidationError:
            return response("", 400)
        except:  # catch database errors
            return response("", 500)

    def patch(self, id):
        schema = ProductSchema()
        try:
            schema.load(request.json)
            query = db.Session.query(Product).filter(
                Product.id == id)
            if query.first() is not None:
                query.update(request.json)
                db.Session.commit()
                return response("", 200)
            return response("", 404)
        except (ValidationError, AssertionError):
            return response("", 400)
        except:  # catch db exceptions
            return response("", 500)

    def delete(self, id):
        try:
            query = db.Session.query(Product).filter(
                Product.id == id)
            if query.first() is not None:
                query.delete()
                db.Session.commit()
                return response("", 200)
            return response("", 404)
        except: # catch db exceptions
            return response("", 500)
