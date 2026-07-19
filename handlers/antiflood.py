# ============================================================
# 🚫 ANTIFLOOD SYSTEM (PRO MAX VERSION)
# ============================================================

import time
import logging
from collections import defaultdict, deque
from pyrogram import filters
from pyrogram.types import Message, ChatPermissions

from database import db

# =========================
# ⚙️ DEFAULT SETTINGS
# =========================
DEFAULT = {
    "limit": 6,
    "window": 5,
    "mute": 60,
    "action": "mute",  # mute / kick / ban
    "enabled": True,
    "delete": True,
    "silent": False
}

settings_collection = db.antiflood_settings
flood_logs = db.flood_logs
warn_db = db.flood_warns
whitelist_db = db.whitelist_users

# =========================
# ⚡ CACHE
# =========================
user_cache = defaultdict(lambda: deque())

# =========================
# 🔧 SETTINGS
# =========================
async def get_settings(chat_id):
    data = await settings_collection.find_one({"chat_id": chat_id})

    if not data:
        DEFAULT["chat_id"] = chat_id
        await settings_collection.insert_one(DEFAULT)
        return DEFAULT

    return data

# =========================
# 👑 CHECK PRIVILEGE
# =========================
async def is_protected(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)

        if member.status in ["administrator", "creator"]:
            return True

        wl = await whitelist_db.find_one({"user_id": user_id})
        return bool(wl)

    except:
        return False

# =========================
# 🚫 FLOOD DETECT
# =========================
async def is_flood(user_id, chat_id):
    settings = await get_settings(chat_id)

    if not settings["enabled"]:
        return False

    now = time.time()
    dq = user_cache[(chat_id, user_id)]

    dq.append(now)

    while dq and now - dq[0] > settings["window"]:
        dq.popleft()

    return len(dq) > settings["limit"]

# =========================
# ⚔️ ACTION SYSTEM
# =========================
async def take_action(client, message, settings):

    user_id = message.from_user.id
    chat_id = message.chat.id

    warns = await warn_db.find_one({"user_id": user_id, "chat_id": chat_id})
    count = warns["count"] + 1 if warns else 1

    await warn_db.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {"$set": {"count": count}},
        upsert=True
    )

    action = settings["action"]

    try:
        if action == "mute":
            duration = settings["mute"] * count

            await message.chat.restrict_member(
                user_id,
                ChatPermissions(),
                until_date=int(time.time()) + duration
            )

        elif action == "kick":
            await message.chat.ban_member(user_id)
            await message.chat.unban_member(user_id)

        elif action == "ban":
            await message.chat.ban_member(user_id)

        if not settings["silent"]:
            await message.reply_text(
                f"🚫 Flood Detected!\n"
                f"👤 {message.from_user.mention}\n"
                f"⚠️ Warn: {count}\n"
                f"⚔️ Action: {action.upper()}"
            )

    except Exception as e:
        logging.error(f"Action error: {e}")

# =========================
# 📊 LOG
# =========================
async def save_log(chat_id, user_id):
    await flood_logs.insert_one({
        "chat_id": chat_id,
        "user_id": user_id,
        "time": time.time()
    })

# =========================
# 🔥 HANDLER
# =========================
def register_antiflood(app):

    @app.on_message(filters.group & ~filters.bot)
    async def handler(client, message: Message):

        if not message.from_user:
            return

        user_id = message.from_user.id
        chat_id = message.chat.id

        # skip admins / whitelist
        if await is_protected(client, chat_id, user_id):
            return

        if await is_flood(user_id, chat_id):

            settings = await get_settings(chat_id)

            # delete message
            if settings["delete"]:
                try:
                    await message.delete()
                except:
                    pass

            await take_action(client, message, settings)
            await save_log(chat_id, user_id)

            user_cache[(chat_id, user_id)].clear()

# =========================
# ⚙️ COMMANDS
# =========================
def register_antiflood_commands(app):

    # TOGGLE
    @app.on_message(filters.command("antiflood") & filters.group)
    async def toggle(client, message: Message):
        data = await get_settings(message.chat.id)
        new = not data["enabled"]

        await settings_collection.update_one(
            {"chat_id": message.chat.id},
            {"$set": {"enabled": new}}
        )

        await message.reply_text(f"⚙️ AntiFlood {'ON 🟢' if new else 'OFF 🔴'}")

    # SET LIMIT
    @app.on_message(filters.command("setflood") & filters.group)
    async def set_flood(client, message: Message):
        try:
            _, l, w = message.text.split()

            await settings_collection.update_one(
                {"chat_id": message.chat.id},
                {"$set": {"limit": int(l), "window": int(w)}},
                upsert=True
            )

            await message.reply_text(f"✅ Limit: {l} | Window: {w}s")
        except:
            await message.reply_text("❌ Usage: /setflood 6 5")

    # SET ACTION
    @app.on_message(filters.command("setaction") & filters.group)
    async def set_action(client, message: Message):
        try:
            _, action = message.text.split()

            if action not in ["mute", "kick", "ban"]:
                return await message.reply_text("❌ mute/kick/ban only")

            await settings_collection.update_one(
                {"chat_id": message.chat.id},
                {"$set": {"action": action}},
                upsert=True
            )

            await message.reply_text(f"⚔️ Action set: {action}")
        except:
            await message.reply_text("❌ Usage: /setaction mute")

    # STATS
    @app.on_message(filters.command("floodstats") & filters.group)
    async def stats(client, message: Message):
        count = await flood_logs.count_documents({"chat_id": message.chat.id})
        await message.reply_text(f"📊 Total Flood Cases: {count}")
