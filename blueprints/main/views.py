from flask import Blueprint, render_template, redirect, url_for

view = Blueprint("main", __name__, template_folder="templates")


@view.route("/")
def index():
    return render_template("index.html")


@view.route("/dashboard")
def show_dashboard():
    return render_template("dashboard.html")


@view.route("/login")
def login():
    return redirect(url_for("main.index"))


@view.route("/register")
def register():
    return redirect(url_for("main.index"))


@view.route("/logout")
def logout_user():
    return redirect(url_for("main.index"))
