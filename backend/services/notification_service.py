from datetime import datetime
from utils.db_connect import notifications_collection


def create_notification(user_id: str, symbol: str, message: str):
    doc = {
        "user_id": user_id,
        "symbol": symbol,
        "message": message,
        "created_at": datetime.utcnow(),
        "read": False,
    }
    notifications_collection.insert_one(doc)
    return doc


def get_unread_notifications(user_id: str):
    cursor = notifications_collection.find({"user_id": user_id, "read": False}).sort(
        "created_at", -1
    )
    return [
        {
            "id": str(n.get("_id")),
            "symbol": n.get("symbol"),
            "message": n.get("message"),
            "created_at": n.get("created_at").isoformat() + "Z",
        }
        for n in cursor
    ]


def mark_all_read(user_id: str) -> int:
    res = notifications_collection.update_many(
        {"user_id": user_id, "read": False}, {"$set": {"read": True}}
    )
    return int(res.modified_count)