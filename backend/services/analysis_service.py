import yfinance as yf
import pandas as pd
import numpy as np


def compute_indicators(symbol: str, period: str = "6mo"):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)
    if hist.empty:
        raise ValueError("No historical data available")

    close = hist["Close"].astype(float)

    ma20 = close.rolling(window=20).mean()
    ma50 = close.rolling(window=50).mean()

    delta = close.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    roll_up = pd.Series(gain).rolling(14).mean()
    roll_down = pd.Series(loss).rolling(14).mean()
    rs = roll_up / (roll_down.replace(0, np.nan))
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi = pd.Series(rsi, index=close.index)

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    latest = close.index[-1]
    indicators = {
        "ma20": float(ma20.loc[latest]) if not np.isnan(ma20.loc[latest]) else None,
        "ma50": float(ma50.loc[latest]) if not np.isnan(ma50.loc[latest]) else None,
        "rsi": float(rsi.loc[latest]) if not np.isnan(rsi.loc[latest]) else None,
        "macd": float(macd.loc[latest]) if not np.isnan(macd.loc[latest]) else None,
        "macd_signal": float(signal.loc[latest]) if not np.isnan(signal.loc[latest]) else None,
        "price": float(close.loc[latest]),
    }

    return indicators


def analyze_stock_advanced(symbol: str):
    indicators = compute_indicators(symbol)

    price = indicators["price"]
    ma20 = indicators["ma20"]
    ma50 = indicators["ma50"]
    rsi = indicators["rsi"]
    macd_val = indicators["macd"]
    macd_signal = indicators["macd_signal"]

    score = 0.0
    reasons = []

    if ma20 is not None and ma50 is not None:
        if ma20 > ma50:
            score += 2.0
            reasons.append("MA20 is above MA50 (uptrend)")
        else:
            score -= 2.0
            reasons.append("MA20 is below MA50 (downtrend)")

    if rsi is not None:
        if rsi < 30:
            score += 1.5
            reasons.append("RSI indicates oversold conditions")
        elif rsi > 70:
            score -= 1.5
            reasons.append("RSI indicates overbought conditions")
        else:
            reasons.append("RSI is neutral")

    if macd_val is not None and macd_signal is not None:
        if macd_val > macd_signal:
            score += 1.5
            reasons.append("MACD above signal (bullish momentum)")
        else:
            score -= 1.0
            reasons.append("MACD below signal (bearish momentum)")

    if ma20 is not None and price is not None:
        if price > ma20:
            score += 1.0
            reasons.append("Price above MA20 (near-term strength)")
        else:
            score -= 0.5
            reasons.append("Price below MA20 (near-term weakness)")

    if score >= 3.0:
        signal = "BUY"
    elif score <= -2.0:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "symbol": symbol,
        "indicators": indicators,
        "score": round(float(score), 2),
        "signal": signal,
        "reasons": reasons,
    }