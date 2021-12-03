from flask import Blueprint, session, redirect, url_for, escape, request
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


#@view.route("/<string:user_id>/edit", methods=["GET"])
#def edit(user_id):
#    return "Edit form"


#@view.route("/", methods=["PUT"])
#def update():
#    return "Update one"


#@view.route("/new", methods=["GET"])
#def new():
#    return "Create form"


@view.route("/", methods=["POST"])
def create():
    first_name = escape(request.form.get("first_name"))
    last_name = escape(request.form.get("last_name"))
    email = escape(request.form.get("email"))

    password = request.form.get("password")
    password_hash = generate_password_hash(password)

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password_hash
    }
    db_users.insert_one(user)
    return "", 201


@view.route("/<string:user_id>", methods=["DELETE"])
def destroy(user_id):
    db_users.delete_one({"_id": ObjectId(user_id)})
    return "", 204
