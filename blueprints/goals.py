from flask import Blueprint, session, redirect, url_for, flash, request, render_template
from database import *
from login import require_login
from datetime import datetime
from bson.objectid import ObjectId

routes_goals = Blueprint("goals", __name__, url_prefix="/goals")


@routes_goals.route("/", methods=["POST"])
@require_login
def create():
    user = db_users.find_one({"email": session.get("email")})
    existing_goals = db_goals.find_one({"user": user["_id"]})

    if "update_daily" in request.form:
        amount = request.form.get("amount")
        if not amount:
            flash("There were one or more missing fields!", "danger")
            return redirect(url_for("dashboard.goals"))

        try:
            amount = int(amount)
        except ValueError:
            flash("Invalid input: amount!", "danger")
            return redirect(url_for("dashboard.goals"))

        db_goals.update_one({
            "user": user["_id"],
        }, {
            "$set": {
                "daily_goal": amount,
                "health_goals": existing_goals["health_goals"] if existing_goals else []
            }
        }, upsert=True)
        flash("Daily goal updated!", "success")
    elif "add_goal" in request.form:
        goal_text = request.form.get("goal_text")

        if not goal_text:
            flash("There were one or more missing fields!", "danger")
            return redirect(url_for("goals.new"))

        db_goals.update_one({
            "user": user["_id"],
        }, {
            "$set": {
                "daily_goal": existing_goals["daily_goal"] if existing_goals else 0
            },
            "$push": {
                "health_goals": {
                    "_id": ObjectId(),
                    "goal": goal_text,
                    "created_on": datetime.today()
                }
            }
        }, upsert=True)
        flash("Health goal added!", "success")
    return redirect(url_for("dashboard.goals"))


@routes_goals.route("/new", methods=["GET"])
@require_login
def new():
    return render_template("goal_new.html")


@routes_goals.route("/<string:item_id>", methods=["DELETE"])
@require_login
def destroy(item_id):
    user = db_users.find_one({"email": session.get("email")})

    db_goals.update_one({
        "user": user["_id"],
    }, {
        "$pull": {
            "health_goals": {
                "_id": ObjectId(item_id)
            }
        }
    })
    return "", 204
