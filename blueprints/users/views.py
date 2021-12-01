from flask import Blueprint

view = Blueprint("users", __name__, url_prefix="/users")


@view.route("/")
def index():
    pass
