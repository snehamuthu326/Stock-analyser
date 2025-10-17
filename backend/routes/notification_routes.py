from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.notification_service import get_unread_notifications, mark_all_read

notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/notifications/unread", methods=["GET"])
@jwt_required()
def unread_notifications():
    user_id = get_jwt_identity()
    data = get_unread_notifications(user_id)
    return jsonify(data)


@notification_bp.route("/notifications/mark_all_read", methods=["POST"])
@jwt_required()
def mark_notifications_read():
    user_id = get_jwt_identity()
    count = mark_all_read(user_id)
    return jsonify({"updated": count})