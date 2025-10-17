# backend/app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, join_room
from routes.auth_routes import auth_bp
from routes.stock_routes import stock_bp
from routes.watchlist_routes import watchlist_bp
from routes.notification_routes import notification_bp
from config import JWT_SECRET_KEY

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(stock_bp, url_prefix="/api")
app.register_blueprint(watchlist_bp, url_prefix="/api")
app.register_blueprint(notification_bp, url_prefix="/api")


@socketio.on("join", namespace="/alerts")
def handle_join(data):
    user_id = (data or {}).get("userId")
    if user_id:
        join_room(user_id)

if __name__ == "__main__":
    # Lazy import to avoid circular imports
    from background_jobs.stock_monitor import start_price_monitor
    start_price_monitor(socketio)
    socketio.run(app, debug=True)
