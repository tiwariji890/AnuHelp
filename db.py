# ============================================================
# 🤖 Group Manager Bot - Database Layer (FINAL ULTIMATE + ANTIRAID)
# ============================================================

import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging
from datetime import datetime

# ============================================================
# 🔗 MongoDB Connection
# ============================================================

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

logging.basicConfig(level=logging.INFO)
logging.info("✅ MongoDB initialized successfully")

# ============================================================
# ⚙️ DEFAULT SETTINGS
# ============================================================

DEFAULT_SETTINGS = {
    "warn_limit": 3,
    "antiedit": False,
    "antiedit_mode": "all",
    "nsfw": False,
    "nsfw_mode": "all",
    "welcome": True
}

# ==========================================================
# 🟢 WELCOME SYSTEM
# ==========================================================

async def set_welcome_message(chat_id: int, text: str):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"message": text}},
        upsert=True
    )

async def get_welcome_message(chat_id: int):
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("message") if data else None

async def set_welcome_status(chat_id: int, status: bool):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_welcome_status(chat_id: int) -> bool:
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("enabled", True) if data else True

# ==========================================================
# 🔒 LOCK SYSTEM
# ==========================================================

async def set_lock(chat_id: int, lock_type: str, status: bool):
    await db.locks.update_one(
        {"chat_id": chat_id},
        {"$set": {f"locks.{lock_type}": status}},
        upsert=True
    )

async def get_locks(chat_id: int):
    data = await db.locks.find_one({"chat_id": chat_id})
    return data.get("locks", {}) if data else {}

# ==========================================================
# ⚠️ WARN SYSTEM
# ==========================================================

async def add_warn(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    warns = data.get("count", 0) + 1 if data else 1

    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": warns}},
        upsert=True
    )
    return warns

async def get_warns(chat_id: int, user_id: int) -> int:
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    return data.get("count", 0) if data else 0

async def reset_warns(chat_id: int, user_id: int):
    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": 0}},
        upsert=True
    )

# ==========================================================
# ⚠️ WARN LIMIT SYSTEM
# ==========================================================

async def set_warn_limit(chat_id: int, limit: int):
    await db.settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"warn_limit": limit}},
        upsert=True
    )

async def get_warn_limit(chat_id: int) -> int:
    data = await db.settings.find_one({"chat_id": chat_id})
    return data.get("warn_limit", DEFAULT_SETTINGS["warn_limit"]) if data else DEFAULT_SETTINGS["warn_limit"]

# ==========================================================
# 🔞 NSFW SYSTEM
# ==========================================================

async def set_nsfw(chat_id: int, status: bool):
    await db.nsfw.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_nsfw(chat_id: int) -> bool:
    data = await db.nsfw.find_one({"chat_id": chat_id})
    return data.get("enabled", DEFAULT_SETTINGS["nsfw"]) if data else DEFAULT_SETTINGS["nsfw"]

async def set_nsfw_mode(chat_id: int, mode: str):
    await db.nsfw.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True
    )

async def get_nsfw_mode(chat_id: int) -> str:
    data = await db.nsfw.find_one({"chat_id": chat_id})
    return data.get("mode", DEFAULT_SETTINGS["nsfw_mode"]) if data else DEFAULT_SETTINGS["nsfw_mode"]

# ==========================================================
# ✏️ ANTI EDIT SYSTEM
# ==========================================================

async def set_antiedit(chat_id: int, status: bool):
    await db.antiedit.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_antiedit(chat_id: int) -> bool:
    data = await db.antiedit.find_one({"chat_id": chat_id})
    return data.get("enabled", DEFAULT_SETTINGS["antiedit"]) if data else DEFAULT_SETTINGS["antiedit"]

async def set_antiedit_mode(chat_id: int, mode: str):
    await db.antiedit.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True
    )

async def get_antiedit_mode(chat_id: int) -> str:
    data = await db.antiedit.find_one({"chat_id": chat_id})
    return data.get("mode", DEFAULT_SETTINGS["antiedit_mode"]) if data else DEFAULT_SETTINGS["antiedit_mode"]

# ==========================================================
# 🧾 LOG SYSTEM
# ==========================================================

async def add_log(chat_id: int, action: str, user_id: int):
    await db.logs.insert_one({
        "chat_id": chat_id,
        "action": action,
        "user_id": user_id,
        "time": datetime.utcnow()
    })

async def get_logs(chat_id: int, limit: int = 10):
    logs = []
    async for log in db.logs.find({"chat_id": chat_id}).sort("_id", -1).limit(limit):
        logs.append(log)
    return logs

# ==========================================================
# 🗑 AUTO DELETE SYSTEM
# ==========================================================

async def set_autodelete(chat_id: int, delay: int, mode: str = "all"):
    await db.autodel.update_one(
        {"chat_id": chat_id},
        {"$set": {"delay": delay, "mode": mode}},
        upsert=True
    )

async def get_autodelete(chat_id: int):
    data = await db.autodel.find_one({"chat_id": chat_id})
    if data:
        return data.get("delay"), data.get("mode", "all")
    return None, None

async def disable_autodelete(chat_id: int):
    await db.autodel.delete_one({"chat_id": chat_id})

async def get_all_autodelete_chats():
    chats = {}
    async for data in db.autodel.find():
        chats[data["chat_id"]] = {
            "delay": data.get("delay"),
            "mode": data.get("mode", "all")
        }
    return chats

# ==========================================================
# 🚨 ANTIRAID SYSTEM (🔥 NEW)
# ==========================================================

async def get_antiraid_config(chat_id: int):
    data = await db.antiraid.find_one({"chat_id": chat_id})
    if not data:
        return {
            "enabled_until": None,
            "raid_time": 21600,
            "ban_time": 3600,
            "auto_trigger": 0
        }
    return data

async def enable_antiraid(chat_id: int, until):
    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled_until": until}},
        upsert=True
    )

async def disable_antiraid(chat_id: int):
    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled_until": None}},
        upsert=True
    )

async def set_raid_time(chat_id: int, seconds: int):
    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"raid_time": seconds}},
        upsert=True
    )

async def set_ban_time(chat_id: int, seconds: int):
    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"ban_time": seconds}},
        upsert=True
    )

async def set_auto_trigger(chat_id: int, value: int):
    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"auto_trigger": value}},
        upsert=True
    )

# ==========================================================
# 🧹 CLEANUP SYSTEM
# ==========================================================

async def clear_group_data(chat_id: int):
    await db.welcome.delete_one({"chat_id": chat_id})
    await db.locks.delete_one({"chat_id": chat_id})
    await db.warns.delete_many({"chat_id": chat_id})
    await db.logs.delete_many({"chat_id": chat_id})
    await db.settings.delete_one({"chat_id": chat_id})
    await db.nsfw.delete_one({"chat_id": chat_id})
    await db.antiedit.delete_one({"chat_id": chat_id})
    await db.autodel.delete_one({"chat_id": chat_id})
    await db.antiraid.delete_one({"chat_id": chat_id})

# ==========================================================
# 📌 INDEXES
# ==========================================================

async def create_indexes():
    await db.warns.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    await db.logs.create_index([("chat_id", 1)])
    await db.antiedit.create_index([("chat_id", 1)])
    await db.nsfw.create_index([("chat_id", 1)])

    await db.autodel.create_index(
        [("chat_id", 1)],
        unique=True
    )

    # 🚨 ANTIRAID INDEX
    await db.antiraid.create_index(
        [("chat_id", 1)],
        unique=True
    )

    logging.info("🚀 All indexes created successfully")
