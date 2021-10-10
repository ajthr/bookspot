from functools import wraps
from flask import make_response as response

from config.utils import get_user, get_staff


def authorized_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        user = get_user()
        if user is not None:
            return func(*args, **kwargs)
        return response("", 401)
    return decorated_func


def staff_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        staff = get_staff()
        if staff is not None:
            return func(*args, **kwargs)
        return response("", 401)
    return decorated_func


def admin_only(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        staff = get_staff()
        if staff is not None:
            if staff.is_admin:
                return func(*args, **kwargs)
        return response("", 401)
    return decorated_func
