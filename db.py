# ============================================================
# 🤖 DATABASE LAYER (ULTRA PRO MAX FINAL + LANGUAGE + SUDO)
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
# ⚡ SIMPLE CACHE
# ============================================================

CACHE = {}

def cache_get(key):
    return CACHE.get(key)

def cache_set(key, value):
    CACHE[key] = value

def cache_del(key):
    CACHE.pop(key, None)

# ============================================================
# ⚙️ DEFAULT SETTINGS
# ============================================================

DEFAULT = {
    "warn_limit": 3,
    "nsfw": False,
    "antiedit": False,
    "welcome": True,
    "locks": [],
    "pinned": None,
    "antibiolink": False,
    "captcha": True
}

# ==========================================================
# 👑 SUDO SYSTEM (NEW 🔥)
# ==========================================================

async def add_sudo(user_id):
    await db.sudo.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def remove_sudo(user_id):
    await db.sudo.delete_one({"user_id": user_id})

async def get_sudo_users():
    users = []
    async for user in db.sudo.find():
        users.append(user["user_id"])
    return users

async def is_sudo_user(user_id):
    user = await db.sudo.find_one({"user_id": user_id})
    return bool(user)

# ==========================================================
# 🌍 LANGUAGE SYSTEM
# ==========================================================

async def set_language(chat_id, lang):
    await db.language.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang, "updated": datetime.utcnow()}},
        upsert=True
    )
    cache_set(f"lang:{chat_id}", lang)


async def get_language(chat_id):
    cached = cache_get(f"lang:{chat_id}")
    if cached is not None:
        return cached

    data = await db.language.find_one({"chat_id": chat_id})
    lang = data.get("lang", "en") if data else "en"

    cache_set(f"lang:{chat_id}", lang)
    return lang


async def delete_language(chat_id):
    await db.language.delete_one({"chat_id": chat_id})
    cache_del(f"lang:{chat_id}")

# ==========================================================
# 🔐 CAPTCHA SYSTEM
# ==========================================================

async def set_captcha(chat_id, status):
    await db.captcha_settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status, "updated": datetime.utcnow()}},
        upsert=True
    )
    cache_set(f"captcha:{chat_id}", status)


async def get_captcha(chat_id):
    cached = cache_get(f"captcha:{chat_id}")
    if cached is not None:
        return cached

    data = await db.captcha_settings.find_one({"chat_id": chat_id})
    status = data.get("enabled", DEFAULT["captcha"]) if data else DEFAULT["captcha"]

    cache_set(f"captcha:{chat_id}", status)
    return status

# ==========================================================
# 🚫 ANTIBIOLINK
# ==========================================================

async def set_antibiolink(chat_id, status):
    await db.antibiolink.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status, "updated": datetime.utcnow()}},
        upsert=True
    )
    cache_set(f"antibiolink:{chat_id}", status)


async def get_antibiolink(chat_id):
    cached = cache_get(f"antibiolink:{chat_id}")
    if cached is not None:
        return cached

    data = await db.antibiolink.find_one({"chat_id": chat_id})
    status = data.get("enabled", DEFAULT["antibiolink"]) if data else DEFAULT["antibiolink"]

    cache_set(f"antibiolink:{chat_id}", status)
    return status

# ==========================================================
# 📌 PINS
# ==========================================================

async def set_pinned(chat_id, message_id):
    await db.pins.update_one(
        {"chat_id": chat_id},
        {"$set": {"message_id": message_id}},
        upsert=True
    )
    cache_set(f"pin:{chat_id}", message_id)


async def get_pinned(chat_id):
    cached = cache_get(f"pin:{chat_id}")
    if cached is not None:
        return cached

    data = await db.pins.find_one({"chat_id": chat_id})
    msg_id = data.get("message_id") if data else None

    cache_set(f"pin:{chat_id}", msg_id)
    return msg_id

# ==========================================================
# 🔐 LOCKS
# ==========================================================

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
# ⚠️ WARN SYSTEM
# ==========================================================

async def add_warn(chat_id, user_id):
    data = await db.warns.find_one({"chat_id": chat_id, "user_id": user_id})
    count = data.get("count", 0) + 1 if data else 1

    await db.warns.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": count}},
        upsert=True
    )

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
# 🚨 ANTIRAID
# ==========================================================

async def enable_antiraid(chat_id, duration):
    until = int(datetime.utcnow().timestamp()) + duration

    await db.antiraid.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled_until": until}},
        upsert=True
    )


async def is_antiraid_active(chat_id):
    data = await db.antiraid.find_one({"chat_id": chat_id})
    if not data:
        return False

    return data.get("enabled_until", 0) > int(datetime.utcnow().timestamp())

# ==========================================================
# 🗑 CAPTCHA DATA STORE
# ==========================================================

async def save_captcha(chat_id, user_id, captcha):
    await db.captcha.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {
            "captcha": captcha,
            "verified": False,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )


async def verify_captcha_user(chat_id, user_id):
    await db.captcha.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"verified": True}}
    )


async def delete_captcha(chat_id, user_id):
    await db.captcha.delete_one({"chat_id": chat_id, "user_id": user_id})

# ==========================================================
# 📌 INDEXES (OPTIMIZED 🔥)
# ==========================================================

async def create_indexes():

    await db.sudo.create_index([("user_id", 1)], unique=True)

    await db.warns.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    await db.antiraid.create_index([("chat_id", 1)], unique=True)
    await db.locks.create_index([("chat_id", 1)], unique=True)
    await db.pins.create_index([("chat_id", 1)], unique=True)
    await db.antibiolink.create_index([("chat_id", 1)], unique=True)

    await db.language.create_index([("chat_id", 1)], unique=True)

    await db.captcha.create_index(
        [("chat_id", 1), ("user_id", 1)],
        unique=True
    )

    await db.captcha.create_index(
        "created_at",
        expireAfterSeconds=300
    )

    logger.info("🚀 All Indexes Created")
