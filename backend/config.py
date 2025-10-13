# backend/config.py
import os

MONGO_URI = os.getenv("mongodb+srv://snehamarimuthu326_db_user:mongodb@stockanalyser.ft0lc2l.mongodb.net/?retryWrites=true&w=majority&appName=StockAnalyser")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwtkey")
