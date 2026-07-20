# ============================================================
# 🤖 DATABASE LAYER (FINAL PRO MAX + SAFE + FAST)
# ============================================================

import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DB")

# ============================================================
# 🔗 CONNECT
# ============================================================

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

logger.info("✅ MongoDB Connected")

# ============================================================
# ⚡ SIMPLE CACHE (BOOST SPEED)
# ============================================================

CACHE = {}

def cache_get(key):
    return CACHE.get(key)

def cache_set(key, value):
    CACHE[key] = value


# ============================================================
# ⚙️ DEFAULT SETTINGS
# ============================================================

DEFAULT = {
    "warn_limit": 3,
    "nsfw": False,
    "antiedit": False,
    "welcome": True,
    "locks": [],
    "pinned": None
}

# ==========================================================
# 📌 PINS SYSTEM (SAVE + RESTORE)
# ==========================================================

async def set_pinned(chat_id, message_id):
    await db.pins.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "message_id": message_id,
            "updated": datetime.utcnow()
        }},
        upsert=True
    )
    cache_set(f"pin:{chat_id}", message_id)


async def get_pinned(chat_id):
    cached = cache_get(f"pin:{chat_id}")
    if cached:
        return cached

    data = await db.pins.find_one({"chat_id": chat_id})
    msg_id = data.get("message_id") if data else None

    cache_set(f"pin:{chat_id}", msg_id)
    return msg_id


async def clear_pinned(chat_id):
    await db.pins.delete_one({"chat_id": chat_id})
    CACHE.pop(f"pin:{chat_id}", None)


# ==========================================================
# 🔐 LOCKS SYSTEM (MULTI LOCK SUPPORT)
# ==========================================================

async def set_lock(chat_id, lock_type):
    data = await db.locks.find_one({"chat_id": chat_id})
    locks = data.get("locks", []) if data else []

    if lock_type not in locks:
        locks.append(lock_type)

    await db.locks.update_one(
        {"chat_id": chat_id},
        {"$set": {"locks": locks}},
        upsert=True
    )

    cache_set(f"locks:{chat_id}", locks)


async def remove_lock(chat_id, lock_type):
    data = await db.locks.find_one({"chat_id": chat_id})
    if not data:
        return

    locks = data.get("locks", [])
    if lock_type in locks:
        locks.remove(lock_type)

    await db.locks.update_one(
        {"chat_id": chat_id},
        {"$set": {"locks": locks}},
        upsert=True
    )

    cache_set(f"locks:{chat_id}", locks)


async def get_locks(chat_id):
    cached = cache_get(f"locks:{chat_id}")
    if cached is not None:
        return cached

    data = await db.locks.find_one({"chat_id": chat_id})
    locks = data.get("locks", []) if data else []

    cache_set(f"locks:{chat_id}", locks)
    return locks


async def is_locked(chat_id, lock_type):
    locks = await get_locks(chat_id)
    return lock_type in locks


# ==========================================================
# ⚠️ WARN
# ==========================================================

async def add_warn(chat_id, user_id):
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    count = data.get("count", 0) + 1 if data else 1

    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": count, "updated": datetime.utcnow()}},
        upsert=True
    )

    cache_set(f"warn:{chat_id}:{user_id}", count)
    return count


async def get_warn(chat_id, user_id):
    cached = cache_get(f"warn:{chat_id}:{user_id}")
    if cached is not None:
        return cached

    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    count = data.get("count", 0) if data else 0

    cache_set(f"warn:{chat_id}:{user_id}", count)
    return count


# ==========================================================
# 🔞 NSFW
# ==========================================================

async def set_nsfw(chat_id, status):
    await db.nsfw.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )
    cache_set(f"nsfw:{chat_id}", status)


async def get_nsfw(chat_id):
    cached = cache_get(f"nsfw:{chat_id}")
    if cached is not None:
        return cached

    data = await db.nsfw.find_one({"chat_id": chat_id})
    status = data.get("enabled", DEFAULT["nsfw"]) if data else DEFAULT["nsfw"]

    cache_set(f"nsfw:{chat_id}", status)
    return status


# ==========================================================
# ✏️ ANTIEDIT
# ==========================================================

async def set_antiedit(chat_id, status):
    await db.antiedit.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )
    cache_set(f"antiedit:{chat_id}", status)


async def get_antiedit(chat_id):
    cached = cache_get(f"antiedit:{chat_id}")
    if cached is not None:
        return cached

    data = await db.antiedit.find_one({"chat_id": chat_id})
    status = data.get("enabled", DEFAULT["antiedit"]) if data else DEFAULT["antiedit"]

    cache_set(f"antiedit:{chat_id}", status)
    return status


# ==========================================================
# 🚨 ANTIRAID
# ==========================================================

async def enable_antiraid(chat_id, duration):
    until = int(datetime.utcnow().timestamp()) + duration

    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "enabled_until": until,
            "updated": datetime.utcnow()
        }},
        upsert=True
    )


async def is_antiraid_active(chat_id):
    data = await db.antiraid.find_one({"chat_id": chat_id})
    if not data:
        return False

    return data.get("enabled_until", 0) > int(datetime.utcnow().timestamp())


# ==========================================================
# 🧾 LOG
# ==========================================================

async def add_log(chat_id, action, user_id):
    await db.logs.insert_one({
        "chat_id": chat_id,
        "action": action,
        "user_id": user_id,
        "time": datetime.utcnow()
    })


# ==========================================================
# 🗑 AUTO DELETE
# ==========================================================

async def set_autodel(chat_id, delay):
    await db.autodel.update_one(
        {"chat_id": chat_id},
        {"$set": {"delay": delay}},
        upsert=True
    )


async def get_autodel(chat_id):
    data = await db.autodel.find_one({"chat_id": chat_id})
    return data.get("delay") if data else None


# ==========================================================
# 📌 INDEXES (VERY IMPORTANT)
# ==========================================================

async def create_indexes():
    await db.warns.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    await db.nsfw.create_index([("chat_id", 1)])
    await db.antiedit.create_index([("chat_id", 1)])
    await db.antiraid.create_index([("chat_id", 1)], unique=True)
    await db.autodel.create_index([("chat_id", 1)], unique=True)

    # 🔥 NEW INDEXES
    await db.locks.create_index([("chat_id", 1)], unique=True)
    await db.pins.create_index([("chat_id", 1)], unique=True)

    logger.info("🚀 Indexes Created")
