from flask import Blueprint, redirect, url_for, request, flash
from database import *

from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

view = Blueprint("users", __name__, url_prefix="/users")


@view.route("/", methods=["GET"])
def index():
    users = db_users.find({}, {"password": 0})
    return dumps(users)


@view.route("/<string:user_id>", methods=["GET"])
def show(user_id):
    user = db_users.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    return dumps(user)


@view.route("/", methods=["POST"])
def create():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("One or more required fields were missing!", "danger")
        return redirect(url_for("main.register"))

    existing_user = db_users.find_one({"email": email})
    if existing_user:
        flash("An account with that email already exists!", "danger")
        return redirect(url_for("main.register"))

    password_hash = generate_password_hash(password)

    user = {
        "name": name,
        "email": email,
        "password": password_hash
    }
    db_users.insert_one(user)
    return redirect(url_for("main.login"))


@view.route("/<string:user_id>", methods=["DELETE"])
def destroy(user_id):
    db_users.delete_one({"_id": ObjectId(user_id)})
    return "", 204
