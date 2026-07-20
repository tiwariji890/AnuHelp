# ============================================================
# 🔒 LOCK SYSTEM (ULTIMATE ROSE STYLE)
# ============================================================

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
import re

from database import set_lock, get_locks

# ============================================================
# 🔐 AVAILABLE LOCKS
# ============================================================

LOCK_TYPES = [
    "all", "media", "photo", "video", "audio", "voice",
    "document", "sticker", "gif",
    "link", "forward", "bots",
    "inline", "game", "location",
    "contact", "poll", "service",
    "text", "url", "hashtag"
]

# ============================================================
# 🔧 ADMIN CHECK
# ============================================================

async def is_admin(client, chat_id, user_id):
    member = await client.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

# ============================================================
# 🔒 LOCK COMMAND
# ============================================================

@Client.on_message(filters.command("lock") & filters.group)
async def lock_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(f"❌ Usage: /lock <type>")

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Admin only")

    lock_type = message.command[1].lower()

    if lock_type not in LOCK_TYPES:
        return await message.reply_text(f"❌ Invalid lock type")

    await set_lock(message.chat.id, lock_type, True)
    await message.reply_text(f"🔒 **Locked:** {lock_type}")

# ============================================================
# 🔓 UNLOCK COMMAND
# ============================================================

@Client.on_message(filters.command("unlock") & filters.group)
async def unlock_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(f"❌ Usage: /unlock <type>")

    if not await is_admin(client, message.chat.id, message.from_user.id):
        return await message.reply_text("❌ Admin only")

    lock_type = message.command[1].lower()

    if lock_type not in LOCK_TYPES:
        return await message.reply_text("❌ Invalid lock")

    await set_lock(message.chat.id, lock_type, False)
    await message.reply_text(f"🔓 **Unlocked:** {lock_type}")

# ============================================================
# 📊 LOCK STATUS
# ============================================================

@Client.on_message(filters.command("locks") & filters.group)
async def locks_status(client: Client, message: Message):
    data = await get_locks(message.chat.id)

    text = "🔒 **Lock Status:**\n\n"

    for lock in LOCK_TYPES:
        status = "✅" if data.get(lock) else "❌"
        text += f"• {lock}: {status}\n"

    await message.reply_text(text)

# ============================================================
# 🚫 LINK DETECTION
# ============================================================

LINK_REGEX = re.compile(r"(https?://|t\.me/|www\.)")

def has_link(text):
    return bool(text and LINK_REGEX.search(text))

# ============================================================
# 🚨 MAIN FILTER (AUTO DELETE)
# ============================================================

@Client.on_message(filters.group & ~filters.service)
async def lock_filter(client: Client, message: Message):

    # skip admins
    if message.from_user:
        if await is_admin(client, message.chat.id, message.from_user.id):
            return

    locks = await get_locks(message.chat.id)

    delete = False

    # GLOBAL LOCK
    if locks.get("all"):
        delete = True

    # MEDIA
    if locks.get("media") and message.media:
        delete = True

    if locks.get("photo") and message.photo:
        delete = True

    if locks.get("video") and message.video:
        delete = True

    if locks.get("audio") and message.audio:
        delete = True

    if locks.get("voice") and message.voice:
        delete = True

    if locks.get("document") and message.document:
        delete = True

    if locks.get("sticker") and message.sticker:
        delete = True

    if locks.get("gif") and message.animation:
        delete = True

    # TEXT
    if locks.get("text") and message.text:
        delete = True

    # LINKS
    if locks.get("link") and (has_link(message.text) or has_link(message.caption)):
        delete = True

    # FORWARD
    if locks.get("forward") and message.forward_date:
        delete = True

    # BOT
    if locks.get("bots") and message.from_user and message.from_user.is_bot:
        delete = True

    # HASHTAG
    if locks.get("hashtag") and message.text and "#" in message.text:
        delete = True

    # CONTACT
    if locks.get("contact") and message.contact:
        delete = True

    # LOCATION
    if locks.get("location") and message.location:
        delete = True

    # POLL
    if locks.get("poll") and message.poll:
        delete = True

    # GAME
    if locks.get("game") and message.game:
        delete = True

    # INLINE
    if locks.get("inline") and message.via_bot:
        delete = True

    # ========================================================
    # 🚫 DELETE ACTION
    # ========================================================

    if delete:
        try:
            await message.delete()
        except:
            pass
