from flask import Blueprint, session, redirect, url_for, request, flash
from database import *
from bson.objectid import ObjectId

from datetime import datetime
from login import require_login

view = Blueprint("items", __name__, url_prefix="/items")


@view.route("/", methods=["POST"])
@require_login
def create():
    user = db_users.find_one({"email": session.get("email")})
    item_name = request.form.get("item_name")
    item_calories = request.form.get("item_calories")
    if not item_name or not item_calories:
        flash("There were one or more missing fields!", "danger")
        return redirect(url_for("dashboard.overview"))

    try:
        item_calories = int(item_calories)
    except ValueError:
        flash("Invalid input: calories!", "danger")
        return redirect(url_for("dashboard.overview"))

    db_items.insert_one({
        "user": user["_id"],
        "name": item_name,
        "calories": item_calories,
        "created_on": datetime.today()
    })
    return redirect(url_for("dashboard.overview"))


@view.route("/<string:user_id>", methods=["DELETE"])
@require_login
def destroy(user_id):
    db_items.delete_one({"_id": ObjectId(user_id)})
    return "", 204
