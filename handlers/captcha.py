# ============================================================
# 🤖 CAPTCHA SYSTEM (FINAL PRO MAX - FIXED + OPTIMIZED)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
import asyncio
import random
import string

from config import OWNER_ID, DEV_LIST, IGNORE_DEVS
from database import db

# ============================================================
# ⚙️ SETTINGS
# ============================================================

CAPTCHA_TIMEOUT = 60  # seconds

# ============================================================
# 🧠 GENERATE CAPTCHA
# ============================================================

def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# ============================================================
# 🚫 NEW USER JOIN
# ============================================================

@Client.on_message(filters.new_chat_members)
async def captcha_join(client, message):
    chat_id = message.chat.id

    for user in message.new_chat_members:

        if user.is_bot:
            continue

        if user.id == OWNER_ID or (IGNORE_DEVS and user.id in DEV_LIST):
            continue

        # Check if already exists (anti-duplicate)
        existing = await db.captcha.find_one({
            "chat_id": chat_id,
            "user_id": user.id
        })

        if existing and not existing.get("verified"):
            continue

        captcha_text = generate_captcha()

        # Restrict user (full mute)
        await client.restrict_chat_member(
            chat_id,
            user.id,
            ChatPermissions()
        )

        # Save in DB
        await db.captcha.update_one(
            {"chat_id": chat_id, "user_id": user.id},
            {"$set": {
                "captcha": captcha_text,
                "verified": False
            }},
            upsert=True
        )

        msg = await message.reply(
            f"🔐 Welcome {user.mention}\n\n"
            f"👉 Verify yourself!\n"
            f"Captcha: `{captcha_text}`\n\n"
            f"Click button below 👇",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ Verify", callback_data=f"verify_{user.id}")]]
            )
        )

        # Timeout system
        await asyncio.sleep(CAPTCHA_TIMEOUT)

        data = await db.captcha.find_one({"chat_id": chat_id, "user_id": user.id})

        if data and not data.get("verified"):
            try:
                await client.ban_chat_member(chat_id, user.id)
                await msg.edit(f"❌ {user.mention} failed captcha → kicked!")
            except:
                pass


# ============================================================
# ✅ VERIFY BUTTON
# ============================================================

@Client.on_callback_query(filters.regex("^verify_"))
async def verify_captcha(client, callback):
    user_id = int(callback.data.split("_")[1])
    chat_id = callback.message.chat.id

    if callback.from_user.id != user_id:
        return await callback.answer("❌ Not your captcha!", show_alert=True)

    data = await db.captcha.find_one({"chat_id": chat_id, "user_id": user_id})

    if not data:
        return await callback.answer("❌ Expired captcha!", show_alert=True)

    await callback.message.reply("✍️ Send captcha text to verify")
    await callback.answer()


# ============================================================
# ✍️ TEXT VERIFY
# ============================================================

@Client.on_message(filters.text & filters.group)
async def check_captcha(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    data = await db.captcha.find_one({"chat_id": chat_id, "user_id": user_id})

    if not data or data.get("verified"):
        return

    if message.text.strip().upper() == data.get("captcha"):

        # Mark verified
        await db.captcha.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"verified": True}}
        )

        # Unmute user
        await client.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )

        await message.reply("✅ Verified successfully!")

    else:
        await message.reply("❌ Wrong captcha!")


# ============================================================
# 🔌 REGISTER FUNCTION (IMPORTANT)
# ============================================================

def register_captcha(app):
    # decorators already handle everything
    pass
