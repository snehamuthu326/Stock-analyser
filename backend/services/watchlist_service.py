from utils.db_connect import watchlist_collection


def get_watchlist(user_id: str):
    doc = watchlist_collection.find_one({"user_id": user_id})
    symbols = doc.get("symbols", []) if doc else []
    return symbols


def add_to_watchlist(user_id: str, symbol: str):
    watchlist_collection.update_one(
        {"user_id": user_id},
        {"$addToSet": {"symbols": symbol}},
        upsert=True,
    )


def remove_from_watchlist(user_id: str, symbol: str):
    watchlist_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"symbols": symbol}},
        upsert=True,
    )