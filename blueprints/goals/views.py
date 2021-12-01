from flask import Blueprint

view = Blueprint("goals", __name__, url_prefix="/goals")


@view.route("/")
def index():
    pass
