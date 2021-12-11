from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from database import *
from werkzeug.security import check_password_hash

routes_main = Blueprint("main", __name__)


@routes_main.route("/")
def index():
    return render_template("index.html")


@routes_main.route("/login")
def login():
    if session.get("email"):
        return redirect(url_for("dashboard.overview"))
    return render_template("login.html")


@routes_main.route("/login", methods=["POST"])
def login_user():
    if session.get("email"):
        return redirect(url_for("dashboard.overview"))

    user = db_users.find_one({"email": request.form.get("email")})
    password = request.form.get("password")

    if not user or not check_password_hash(user["password"], password):
        flash("Incorrect login!", "danger")
        return redirect(url_for("main.login"))

    session["email"] = user.get("email", "danger")
    return redirect(url_for("dashboard.overview"))


@routes_main.route("/register")
def register():
    return render_template("register.html")


@routes_main.route("/logout")
def logout_user():
    session.pop("email", None)
    flash("You are now logged out", "success")
    return redirect(url_for("main.login"))
