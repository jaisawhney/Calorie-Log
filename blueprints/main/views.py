from flask import Blueprint, render_template

view = Blueprint("main", __name__, template_folder="templates")


@view.route("/")
def index():
    return render_template("index.html")
