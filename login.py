from flask import session, redirect, url_for, flash
from functools import wraps
from database import *


def require_login(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        email = session.get("email")
        if not email or not db_users.find_one({"email": email}):
            flash("You need to login to do that!", "danger")
            return redirect(url_for("main.login"))
        return function(*args, **kwargs)

    return wrapper
