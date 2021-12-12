import datetime

from flask import Blueprint, render_template, session
from database import *
from login import require_login

routes_dashboard = Blueprint("dashboard", __name__, template_folder="../templates/dashboard")


@routes_dashboard.route("/dashboard")
@require_login
def overview():
    user = db_users.find_one({"email": session.get("email")})

    list_items = list(db_items.find({"user": user["_id"]}))
    daily_stats = list(db_items.aggregate([{
        "$match": {
            "created_on": {
                "$gte": datetime.datetime.today() - datetime.timedelta(days=1)
            },
            "user": user["_id"]
        }
    }, {"$group": {
        "_id": None,
        "amount": {"$sum": "$calories"}
    }}, {"$limit": 1}]))

    goals = db_goals.find_one({"user": user["_id"]})
    daily_goal = goals["daily_goal"] if goals else 0
    daily_calories = daily_stats[0]["amount"] if len(daily_stats) != 0 else 0

    return render_template("overview.html", items=list_items, daily_calories=daily_calories, daily_goal=daily_goal)


@routes_dashboard.route("/dashboard/goals", methods=["GET"])
@require_login
def goals():
    user = db_users.find_one({"email": session.get("email")})

    goals = db_goals.find_one({"user": user["_id"]})
    health_goals = goals["health_goals"] if goals else []
    daily_goal = goals["daily_goal"] if goals else 0
    return render_template("goals.html", health_goals=enumerate(health_goals), daily_goal=daily_goal)
