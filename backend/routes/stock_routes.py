# stock_routes.py
from flask import Blueprint, jsonify
from services.stock_service import get_stock, get_multiple_stocks

stock_bp = Blueprint("stock_bp", __name__)

# Single stock endpoint
@stock_bp.route("/stock/<symbol>", methods=["GET"])
def single_stock(symbol):
    data = get_stock(symbol)
    return jsonify(data)

# Multiple stocks endpoint
@stock_bp.route("/stocks", methods=["GET"])
def multiple_stocks():
    # Example: ?symbols=AAPL,GOOG,MSFT
    from flask import request
    symbols = request.args.get("symbols", "")
    symbols_list = symbols.split(",") if symbols else []
    data = get_multiple_stocks(symbols_list)
    return jsonify(data)
