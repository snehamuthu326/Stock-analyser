# backend/services/auth_service.py
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from utils.db_connect import users_collection

bcrypt = Bcrypt()

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return {"error": "Username already exists"}, 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    users_collection.insert_one({
        "username": username,
        "password": hashed_pw
    })
    return {"message": "User registered successfully"}, 201


def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(
        identity=str(user["_id"]),
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": token, "username": username}, 200
