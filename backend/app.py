# backend/app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from routes.auth_routes import auth_bp
from routes.stock_routes import stock_bp
from config import JWT_SECRET_KEY

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(stock_bp, url_prefix="/api")  

if __name__ == "__main__":
    app.run(debug=True)
