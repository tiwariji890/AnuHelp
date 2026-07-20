# ============================================================
# 📌 PIN SYSTEM (ULTIMATE MODERN)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
import logging

from database import db  # tumhara db file

# ============================================================
# 🔧 AUTO PIN DB FUNCTIONS
# ============================================================

async def set_auto_pin(chat_id: int, status: bool):
    await db.pins.update_one(
        {"chat_id": chat_id},
        {"$set": {"auto_pin": status}},
        upsert=True
    )

async def get_auto_pin(chat_id: int) -> bool:
    data = await db.pins.find_one({"chat_id": chat_id})
    return data.get("auto_pin", False) if data else False

# ============================================================
# 📌 PIN COMMAND
# ============================================================

@Client.on_message(filters.command("pin") & filters.group)
async def pin_message(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a message to pin")

    try:
        await message.reply_to_message.pin(disable_notification=False)
        await message.reply_text("📌 **Message pinned successfully!**")
    except ChatAdminRequired:
        await message.reply_text("❌ I need admin rights to pin messages")

# ============================================================
# 🔕 SILENT PIN
# ============================================================

@Client.on_message(filters.command("pinloud") & filters.group)
async def pin_loud(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a message")

    try:
        await message.reply_to_message.pin(disable_notification=True)
        await message.reply_text("📌 **Pinned silently!**")
    except ChatAdminRequired:
        await message.reply_text("❌ Admin rights required")

# ============================================================
# 📌 UNPIN
# ============================================================

@Client.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client: Client, message: Message):
    try:
        await client.unpin_chat_message(message.chat.id)
        await message.reply_text("📌❌ **Message unpinned!**")
    except ChatAdminRequired:
        await message.reply_text("❌ I need admin rights")

# ============================================================
# 📌 UNPIN ALL
# ============================================================

@Client.on_message(filters.command("unpinall") & filters.group)
async def unpin_all(client: Client, message: Message):
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply_text("🧹 **All pinned messages removed!**")
    except ChatAdminRequired:
        await message.reply_text("❌ Admin rights needed")

# ============================================================
# 🤖 AUTO PIN TOGGLE
# ============================================================

@Client.on_message(filters.command("autopin") & filters.group)
async def auto_pin_toggle(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "⚙️ Usage:\n/autopin on\n/autopin off"
        )

    arg = message.command[1].lower()

    if arg == "on":
        await set_auto_pin(message.chat.id, True)
        await message.reply_text("✅ **Auto Pin Enabled**")
    elif arg == "off":
        await set_auto_pin(message.chat.id, False)
        await message.reply_text("❌ **Auto Pin Disabled**")
    else:
        await message.reply_text("❌ Invalid option")

# ============================================================
# 🤖 AUTO PIN HANDLER
# ============================================================

@Client.on_message(filters.group & ~filters.service)
async def auto_pin_handler(client: Client, message: Message):
    try:
        enabled = await get_auto_pin(message.chat.id)
        if
