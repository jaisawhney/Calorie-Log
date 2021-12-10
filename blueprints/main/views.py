import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, session, request, flash
from database import *
from login import require_login
from werkzeug.security import check_password_hash

view = Blueprint("main", __name__, template_folder="templates")


@view.route("/")
def index():
    return render_template("index.html")


@view.route("/dashboard")
@require_login
def dashboard():
    list_items = list(db_items.find({}, {}))

    daily_stats = list(db_items.aggregate([
        {"$match": {
            "created_on": {
                "$gte": datetime.datetime.today() - datetime.timedelta(days=1)
            }}},
        {"$group": {
            "_id": None,
            "amount": {"$sum": "$calories"}
        }},
        {"$limit": 1}
    ]))
    stats = {
        "daily": daily_stats[0] if len(daily_stats) != 0 else 0
    }

    return render_template("dashboard_overview.html", items=list_items, stats=stats, goals={"daily": {
        "amount": 1000
    }})


@view.route("/login")
def login():
    if session.get("email"):
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@view.route("/login", methods=["POST"])
def login_user():
    if session.get("email"):
        return redirect(url_for("main.dashboard"))

    user = db_users.find_one({"email": request.form.get("email")})
    password = request.form.get("password")

    if not user or not check_password_hash(user["password"], password):
        flash("Incorrect login!", "danger")
        return redirect(url_for("main.login"))

    session["email"] = user.get("email", "danger")
    return redirect(url_for("main.dashboard"))


@view.route("/register")
def register():
    return render_template("register.html")


@view.route("/logout")
def logout_user():
    session.pop("email", None)
    flash("You are now logged out", "success")
    return redirect(url_for("main.login"))
