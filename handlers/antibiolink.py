# ============================================================
# 🚫 ANTI BIO LINK SYSTEM (ULTRA PRO MAX)
# ============================================================

from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import UserNotParticipant
import re

from database import (
    add_warn,
    get_warn
)

from database import db  # direct access for toggle

# ============================================================
# ⚙️ CONFIG
# ============================================================

BIO_LINK_REGEX = r"(https?://|t\.me/|@\w+|www\.)"
WARN_LIMIT = 3

# ============================================================
# 🧠 TOGGLE SYSTEM (DB)
# ============================================================

async def set_antibiolink(chat_id, status):
    await db.antibiolink.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_antibiolink(chat_id):
    data = await db.antibiolink.find_one({"chat_id": chat_id})
    return data.get("enabled", False) if data else False


# ============================================================
# 🔧 COMMANDS
# ============================================================

def register_antibiolink(app):

    # ON/OFF
    @app.on_message(filters.command("antibiolink") & filters.group)
    async def toggle(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: /antibiolink on/off")

        arg = message.command[1].lower()

        if arg == "on":
            await set_antibiolink(message.chat.id, True)
            await message.reply("🚫 Anti Bio Link Enabled")

        elif arg == "off":
            await set_antibiolink(message.chat.id, False)
            await message.reply("✅ Anti Bio Link Disabled")

        else:
            await message.reply("Use: on/off")

    # ========================================================
    # 🚨 MAIN CHECK
    # ========================================================

    @app.on_message(filters.group & filters.text)
    async def check_bio(client, message):

        if not await get_antibiolink(message.chat.id):
            return

        user = message.from_user
        if not user:
            return

        # 🔍 Get Bio
        try:
            full = await client.get_chat(user.id)
            bio = full.bio or ""
        except UserNotParticipant:
            return
        except Exception:
            return

        # 🔗 Check link
        if not re.search(BIO_LINK_REGEX, bio.lower()):
            return

        # ❌ Delete message
        try:
            await message.delete()
        except:
            pass

        # ⚠️ Warn system
        warns = await add_warn(message.chat.id, user.id)

        if warns >= WARN_LIMIT:
            try:
                await client.restrict_chat_member(
                    message.chat.id,
                    user.id,
                    ChatPermissions()
                )
                await message.reply(
                    f"🔕 User muted!\nReason: Bio link\nWarns: {warns}"
                )
            except:
                pass
        else:
            await message.reply(
                f"⚠️ Bio link not allowed!\nWarns: {warns}/3"
            )
