from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.watchlist_service import get_watchlist, add_to_watchlist, remove_from_watchlist

watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.route("/watchlist", methods=["GET"])
@jwt_required()
def list_watchlist():
    user_id = get_jwt_identity()
    items = get_watchlist(user_id)
    return jsonify(items)


@watchlist_bp.route("/watchlist", methods=["POST"])
@jwt_required()
def add_watch():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    symbol = (data.get("symbol") or "").upper().strip()
    if not symbol:
        return {"error": "symbol required"}, 400
    add_to_watchlist(user_id, symbol)
    return {"status": "ok"}


@watchlist_bp.route("/watchlist/<symbol>", methods=["DELETE"])
@jwt_required()
def remove_watch(symbol):
    user_id = get_jwt_identity()
    remove_from_watchlist(user_id, symbol.upper().strip())
    return {"status": "ok"}