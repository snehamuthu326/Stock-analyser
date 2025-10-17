import threading
import time
from typing import Optional

import yfinance as yf

from utils.db_connect import watchlist_collection
from services.notification_service import create_notification


def _check_prices_and_alert(socketio):
    while True:
        try:
            cursor = watchlist_collection.find({})
            for doc in cursor:
                user_id = str(doc.get("user_id"))
                symbols = doc.get("symbols", [])
                for symbol in symbols:
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        price = info.get("regularMarketPrice")
                        prev = info.get("previousClose")
                        if price is None or prev is None:
                            continue
                        change = (price - prev) / prev if prev else 0
                        if abs(change) >= 0.03:
                            direction = "up" if change > 0 else "down"
                            message = f"{symbol} moved {direction} {abs(change)*100:.1f}% to {price}"
                            notif = create_notification(user_id, symbol, message)
                            if socketio is not None:
                                socketio.emit("price_alert", {
                                    "userId": user_id,
                                    "symbol": symbol,
                                    "message": message,
                                }, namespace="/alerts", to=user_id)
                    except Exception:
                        continue
        except Exception:
            pass
        time.sleep(30)


def start_price_monitor(socketio: Optional[object] = None):
    thread = threading.Thread(target=_check_prices_and_alert, args=(socketio,), daemon=True)
    thread.start()