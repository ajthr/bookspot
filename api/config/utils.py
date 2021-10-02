import jwt
import uuid
import pyotp
import emails
from pathlib import Path
from functools import wraps
from emails.template import JinjaTemplate
from flask import request, make_response as response

from config import settings, db

from customers.models import Customer

totp = pyotp.TOTP(s=settings.SECRET_KEY, interval=120)


def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        session_id = request.cookies.get("__USESSID_")
        if session_id is not None:
            try:
                jwt.decode(
                    session_id, settings.SECRET_KEY, algorithms=["HS256"])
                return func(*args, **kwargs)
            except (jwt.exceptions.InvalidTokenError,
                    jwt.exceptions.InvalidSignatureError,
                    jwt.exceptions.ExpiredSignatureError):
                return response("", 401)
        return response("", 401)
    return decorated_func


def signin(name, email):
    try:
        user = db.Session.query(Customer).filter(
            Customer.email == email).first()
        if user is None:
            uid = uuid.uuid4().hex
            exists = db.Session.query(Customer).filter(
                Customer.id == uid).first()
            while exists is not None:
                uid = uuid.uuid4().hex
                exists = db.Session.query(Customer).filter(
                    Customer.id == uid).first()
            user = Customer(id=uid, email=email, name=name)
            db.Session.add(user)
            db.Session.commit()
            token = jwt.encode(
                {"id": user.id}, settings.SECRET_KEY, algorithm="HS256")
            resp = response("", 200)
            resp.set_cookie("__USESSID_", token, httponly=True,
                            secure=True, samesite='strict')
            return resp
        token = jwt.encode(
            {"id": user.id}, settings.SECRET_KEY, algorithm="HS256")
        resp = response("", 200)
        resp.set_cookie("__USESSID_", token, httponly=True,
                        secure=True, samesite='strict')
        return resp
    except:
        return response("", 500)


def get_user():
    try:
        session_id = request.cookies.get("__USESSID_")
        user_id = jwt.decode(
            session_id, settings.SECRET_KEY, algorithms=["HS256"])["id"]
        user = db.Session.query(Customer).filter(
            Customer.id == user_id).first()
        return user
    except:
        return None


def smtp_server(receiver_email, subject, html_content, environment):
    try:
        message = emails.Message(
            subject=JinjaTemplate(subject),
            html=JinjaTemplate(html_content),
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT,
                        "user": settings.SMTP_USER, "password": settings.SMTP_PASSWORD, "ssl": True}
        resp = message.send(
            to=receiver_email, render=environment, smtp=smtp_options)
        return resp
    except:
        return response("", 500)


def send_mail(email, otp):
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "signin.html") as f:
        content = f.read()
    email_response = smtp_server(email, "BookSpot OTP", content, {
                                 "otp": otp})
    if email_response.status_code == 250:
        return response("", 200)
    return response("", 500)
