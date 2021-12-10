import os
from pymongo import MongoClient

host = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/calorie-log")
client = MongoClient(host=host)
db = client.get_default_database()

db_users = db.users
db_goals = db.goals
db_items = db.items
