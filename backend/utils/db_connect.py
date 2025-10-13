# backend/utils/db_connect.py
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["stock_analyzer"]
users_collection = db["users"]
