# ============================================================
# 🤖 APPROVAL SYSTEM (ULTIMATE PRO MAX++)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient
from cachetools import TTLCache
from config import MONGO_URI, DB_NAME, DEV_LIST

# ============================================================
# 📦 DATABASE
# ============================================================

mongo = AsyncIOMotorClient(MONGO_URI)
db = mongo[DB_NAME]
col = db["approvals"]

# ============================================================
# ⚡ CACHE (FAST LOOKUP)
# ============================================================

cache = TTLCache(maxsize=10000, ttl=600)

def clear_cache(chat_id=None):
    if chat_id:
        keys = [k for k in cache if str(chat_id) in k]
        for k in keys:
            cache.pop(k, None)
    else:
        cache.clear()

# ============================================================
# 🔐 ADMIN CHECK
# ============================================================

async def is_admin(client, message: Message):
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# ============================================================
# 🔧 DATABASE FUNCTIONS
# ============================================================

async def approve_user(chat_id, user_id):
    await col.update_one(
        {"chat_id": chat_id},
        {"$addToSet": {"users": user_id}},
        upsert=True
    )

async def unapprove_user(chat_id, user_id):
    await col.update_one(
        {"chat_id": chat_id},
        {"$pull": {"users": user_id}}
    )

async def is_approved(chat_id, user_id):
    key = f"{chat_id}:{user_id}"

    if key in cache:
        return cache[key]

    data = await col.find_one({"chat_id": chat_id})
    result = user_id in data.get("users", []) if data else False

    cache[key] = result
    return result

async def get_all(chat_id):
    key = f"list:{chat_id}"

    if key in cache:
        return cache[key]

    data = await col.find_one({"chat_id": chat_id})
    users = data.get("users", []) if data else []

    cache[key] = users
    return users

async def remove_all(chat_id):
    await col.update_one(
        {"chat_id": chat_id},
        {"$set": {"users": []}},
        upsert=True
    )

# ============================================================
# 🎯 TARGET RESOLVER
# ============================================================

async def get_target(message: Message):
    if message.reply_to_message:
        if message.reply_to_message.sender_chat:
            return message.reply_to_message.sender_chat.id
        if message.reply_to_message.from_user:
            return message.reply_to_message.from_user.id

    if len(message.command) > 1:
        try:
            return int(message.command[1])
        except:
            return None
    return None

# ============================================================
# ✅ APPROVE
# ============================================================

@Client.on_message(filters.command(["approve", "free"]) & filters.group)
async def approve_cmd(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply("❌ Admin only")

    user_id = await get_target(message)

    if not user_id:
        return await message.reply("❌ Reply karo ya ID do")

    if message.from_user and user_id == message.from_user.id:
        return await message.reply("🙃 Khud ko approve nahi kar sakte")

    if user_id in DEV_LIST:
        return await message.reply("👑 Dev already approved")

    if await is_approved(message.chat.id, user_id):
        return await message.reply("⚠️ Already approved")

    await approve_user(message.chat.id, user_id)
    clear_cache(message.chat.id)

    await message.reply(
        f"✅ Approved: `{user_id}`\n🛡️ All protections ignore karega"
    )

# ============================================================
# ❌ UNAPPROVE
# ============================================================

@Client.on_message(filters.command(["unapprove", "unfree"]) & filters.group)
async def unapprove_cmd(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply("❌ Admin only")

    user_id = await get_target(message)

    if not user_id:
        return await message.reply("❌ Reply karo ya ID do")

    if not await is_approved(message.chat.id, user_id):
        return await message.reply("⚠️ User approved nahi hai")

    await unapprove_user(message.chat.id, user_id)
    clear_cache(message.chat.id)

    await message.reply(f"❌ Unapproved: `{user_id}`")

# ============================================================
# 📜 LIST APPROVED USERS
# ============================================================

@Client.on_message(filters.command("approved") & filters.group)
async def approved_list(client: Client, message: Message):

    users = await get_all(message.chat.id)

    if not users:
        return await message.reply("📭 No approved users")

    text = "✅ **Approved Users:**\n\n"

    for i, user in enumerate(users[:50], start=1):
        text += f"{i}. `{user}`\n"

    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑 Clear All", callback_data="clear_approved")]
    ])

    await message.reply(text, reply_markup=btn)

# ============================================================
# 🗑 CLEAR ALL
# ============================================================

@Client.on_callback_query(filters.regex("^clear_approved$"))
async def clear_all_cb(client: Client, cq: CallbackQuery):

    try:
        member = await client.get_chat_member(cq.message.chat.id, cq.from_user.id)
        if member.status not in ["administrator", "creator"]:
            return await cq.answer("❌ Admin only", show_alert=True)
    except:
        return

    await remove_all(cq.message.chat.id)
    clear_cache(cq.message.chat.id)

    await cq.message.edit("🗑 All approved users cleared")
    await cq.answer("Done")

# ============================================================
# 🧹 CLEAR COMMAND
# ============================================================

@Client.on_message(filters.command("clearapproved") & filters.group)
async def clear_cmd(client: Client, message: Message):

    if not await is_admin(client, message):
        return await message.reply("❌ Admin only")

    btn = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Yes", callback_data="clear_approved"),
            InlineKeyboardButton("❌ No", callback_data="cancel")
        ]
    ])

    await message.reply("⚠️ Clear all approved users?", reply_markup=btn)

# ============================================================
# ❌ CANCEL BUTTON
# ============================================================

@Client.on_callback_query(filters.regex("^cancel$"))
async def cancel_cb(_, cq: CallbackQuery):
    await cq.message.edit("❌ Cancelled")
