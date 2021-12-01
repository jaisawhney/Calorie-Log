from flask import Flask

from blueprints.main.views import view as routes_main
from blueprints.goals.views import view as routes_goals
from blueprints.users.views import view as routes_users

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.register_blueprint(routes_main)
app.register_blueprint(routes_goals)
app.register_blueprint(routes_users)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
