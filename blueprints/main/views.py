import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, session
from database import *
from login import require_login

view = Blueprint("main", __name__, template_folder="templates")


@view.route("/")
def index():
    return render_template("index.html")


@view.route("/dashboard")
@require_login
def dashboard():
    list_items = list(db_items.find({}, {}))

    total_stats = list(db_items.aggregate([
        {"$match": {}},
        {"$group": {
            "_id": None,
            "amount": {"$sum": "$calories"}
        }},
        {"$limit": 1}
    ]))

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
        "total": total_stats[0] if len(total_stats) != 0 else 0,
        "daily": daily_stats[0] if len(daily_stats) != 0 else 0
    }

    return render_template("dashboard.html", items=list_items, stats=stats)


@view.route("/login")
def login():
    if session.get("email"):
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")


@view.route("/register")
def register():
    return render_template("register.html")


@view.route("/logout")
def logout_user():
    return redirect(url_for("main.index"))
