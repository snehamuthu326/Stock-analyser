# stock_routes.py
from flask import Blueprint, jsonify, request
from services.stock_service import get_stock, get_multiple_stocks, get_historical
from services.analysis_service import analyze_stock_advanced

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
    symbols = request.args.get("symbols", "")
    symbols_list = symbols.split(",") if symbols else []
    data = get_multiple_stocks(symbols_list)
    return jsonify(data)


@stock_bp.route("/stock/<symbol>/historical", methods=["GET"])
def historical(symbol):
    # optional: ?period=6mo&interval=1d
    period = request.args.get("period", "6mo")
    interval = request.args.get("interval", "1d")
    data = get_historical(symbol, period=period, interval=interval)
    return jsonify(data)


@stock_bp.route("/analyze_stock_advanced", methods=["GET"])
def analyze_stock():
    symbol = request.args.get("symbol", "").upper().strip()
    if not symbol:
        return {"error": "symbol required"}, 400
    result = analyze_stock_advanced(symbol)
    return jsonify(result)
