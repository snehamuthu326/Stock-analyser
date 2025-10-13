# stock_service.py
import yfinance as yf
import pandas as pd

def get_stock(symbol: str):
    """
    Fetch real-time stock info for a single symbol
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get("regularMarketPrice")
        previous_close = info.get("previousClose")
        name = info.get("shortName")
        sector = info.get("sector")
        return {
            "symbol": symbol,
            "name": name,
            "current_price": current_price,
            "previous_close": previous_close,
            "sector": sector
        }
    except Exception as e:
        return {"error": str(e)}

def get_multiple_stocks(symbols: list):
    """
    Fetch summary data for multiple stocks
    """
    data = []
    for symbol in symbols:
        stock_data = get_stock(symbol)
        data.append(stock_data)
    return data
