# backend/config.py
import os

# Read from environment, fall back to localhost for development
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretjwtkey")
