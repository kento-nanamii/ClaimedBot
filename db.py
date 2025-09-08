import os
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["claimedbot"]
users = db["users"]
daily_claims = db["daily_claims"]
banks = db["banks"]

def get_user(user_id):
    user = users.find_one({"_id": user_id})
    if not user:
        users.insert_one({"_id": user_id, "balance": 100})
        return {"_id": user_id, "balance": 100}
    return user
