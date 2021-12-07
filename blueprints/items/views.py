from flask import Blueprint, session, redirect, url_for, escape, request, flash
from database import *
from bson.objectid import ObjectId

from datetime import datetime

view = Blueprint("items", __name__, url_prefix="/items")


@view.route("/", methods=["GET"])
def index():
    pass


@view.route("/<string:user_id>", methods=["GET"])
def show(user_id):
    pass


# @view.route("/<string:user_id>/edit", methods=["GET"])
# def edit(user_id):
#    return "Edit form"


# @view.route("/", methods=["PUT"])
# def update():
#    return "Update one"


# @view.route("/new", methods=["GET"])
# def new():
#    return "Create form"


@view.route("/", methods=["POST"])
def create():
    user = request.form.get("user_id")
    item_name = request.form.get("item_name")

    if not item_name:
        flash("Invalid input: item name!", "danger")
        return redirect(url_for("main.dashboard"))

    try:
        item_calories = int(request.form.get("item_calories"))
    except ValueError:
        flash("Invalid input: calories!", "danger")
        return redirect(url_for("main.dashboard"))

    item = {
        "user": user,
        "name": item_name,
        "calories": item_calories,
        "created_on": datetime.today()
    }
    db_items.insert_one(item)
    return redirect(url_for("main.dashboard"))


@view.route("/<string:user_id>", methods=["DELETE"])
def destroy(user_id):
    db_items.delete_one({"_id": ObjectId(user_id)})
    return "", 204
