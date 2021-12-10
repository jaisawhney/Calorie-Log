from flask import Flask, render_template

from blueprints.main.views import view as routes_main
from blueprints.dashboard.views import view as routes_dashboard
from blueprints.goals.views import view as routes_goals
from blueprints.users.views import view as routes_users
from blueprints.items.views import view as routes_items

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.register_blueprint(routes_main)
app.register_blueprint(routes_dashboard)
app.register_blueprint(routes_goals)
app.register_blueprint(routes_users)
app.register_blueprint(routes_items)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
