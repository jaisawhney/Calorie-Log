from flask import Blueprint, session, redirect, url_for, flash, request
from database import *
from login import require_login

view = Blueprint("goals", __name__, url_prefix="/goals")


@view.route("/", methods=["POST"])
@require_login
def create():
    user = db_users.find_one({"email": session.get("email")})
    amount = request.form.get("amount")
    category = request.form.get("category")

    if not amount or not category or category not in ["daily"]:
        flash("There were one or more missing fields!", "danger")
        return redirect(url_for("dashboard.goals"))

    try:
        amount = int(amount)
    except ValueError:
        flash("Invalid input: amount!", "danger")
        return redirect(url_for("dashboard.goals"))

    db_goals.update_one({
        "user": user["_id"],
        "category": category
    }, {
        "$set": {"amount": amount}
    }, upsert=True)
    flash("Goal updated!", "success")
    return redirect(url_for("dashboard.goals"))
