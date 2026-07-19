# ============================================================
# 🚫 ANTI-EDIT SYSTEM (ULTRA FAST + MONGODB)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from database import add_log
import asyncio

# ============================================================
# ⚡ MEMORY CACHE (ANTI DUPLICATE)
# ============================================================

EDIT_CACHE = {}

# ============================================================
# 🔞 DB FUNCTIONS (LOCAL SIMPLE)
# ============================================================

from database import db

async def set_antiedit(chat_id: int, status: bool):
    await db.antiedit.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_antiedit(chat_id: int) -> bool:
    data = await db.antiedit.find_one({"chat_id": chat_id})
    return data.get("enabled", False) if data else False


# ============================================================
# 🚨 EDIT DETECTION
# ============================================================

@Client.on_edited_message(filters.group)
async def anti_edit_handler(client: Client, message: Message):

    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0

    # ❌ if disabled
    if not await get_antiedit(chat_id):
        return

    # ⚡ anti duplicate
    key = f"{chat_id}_{message.id}"
    if key in EDIT_CACHE:
        return

    EDIT_CACHE[key] = True

    try:
        # ⚡ ultra fast delete
        await asyncio.sleep(0.1)
        await message.delete()

        # 🧾 log
        await add_log(chat_id, "ANTI_EDIT_DELETE", user_id)

        # 💬 stylish alert
        warn = await client.send_message(
            chat_id,
            f"""
🚫 **Edited Message Deleted**

👤 User: {message.from_user.mention if message.from_user else "Unknown"}
⚡ Speed: 0.1s
🛡 Protection: ACTIVE

❌ Editing is not allowed!
"""
        )

        # auto delete alert
        await asyncio.sleep(4)
        await warn.delete()

    except Exception as e:
        print("AntiEdit Error:", e)

    finally:
        await asyncio.sleep(8)
        EDIT_CACHE.pop(key, None)


# ============================================================
# 🎛 COMMANDS
# ============================================================

@Client.on_message(filters.command("antiedit") & filters.group)
async def antiedit_toggle(client: Client, message: Message):

    chat_id = message.chat.id

    # check status
    if len(message.command) == 1:
        status = await get_antiedit(chat_id)
        return await message.reply_text(
            f"🚫 Anti-Edit is {'ON' if status else 'OFF'}"
        )

    arg = message.command[1].lower()

    if arg == "on":
        await set_antiedit(chat_id, True)
        await message.reply_text("✅ Anti-Edit Enabled")

    elif arg == "off":
        await set_antiedit(chat_id, False)
        await message.reply_text("❌ Anti-Edit Disabled")


# ============================================================
# 📦 HANDLER REGISTER (FOR LOADER)
# ============================================================

def register_antiedit(app):
    # decorators already handle everything
    pass
