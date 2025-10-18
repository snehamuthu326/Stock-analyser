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
        day_high = info.get("dayHigh")
        day_low = info.get("dayLow")
        name = info.get("shortName")
        sector = info.get("sector")

        # Keep existing keys for compatibility and add new ones expected by frontend
        return {
            # Core identity
            "symbol": symbol,
            "name": name,
            "sector": sector,

            # Old keys (existing clients)
            "current_price": current_price,
            "previous_close": previous_close,

            # New keys (Dashboard expectations)
            "price": current_price,
            "previousClose": previous_close,
            "high": day_high,
            "low": day_low,
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


def get_historical(symbol: str, period: str = "6mo", interval: str = "1d"):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        hist = hist.reset_index()
        # Normalize to simple list of OHLCV dicts
        records = []
        for _, row in hist.iterrows():
            records.append(
                {
                    "date": getattr(row, "Date", getattr(row, "Datetime", None)).isoformat(),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
                }
            )
        return {"symbol": symbol, "candles": records}
    except Exception as e:
        return {"error": str(e)}
