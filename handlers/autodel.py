# ============================================================
# 🤖 AUTO DELETE + EDIT DELETE SYSTEM (ULTRA PRO MAX FINAL)
# ============================================================

import asyncio
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait

# ============================================================
# 🧠 STORAGE
# ============================================================

auto_delete_chats = {}
auto_delete_modes = {}
pending_tasks = set()

# ============================================================
# ⏱ TIME PARSER
# ============================================================

def parse_time(t: str):
    t = t.lower().strip()
    m = re.match(r'^(\d+)([smhd])$', t)
    if not m:
        return None
    v, u = int(m.group(1)), m.group(2)
    return v * {'s':1,'m':60,'h':3600,'d':86400}[u]


def format_time(s: int):
    if s < 60: return f"{s}s"
    if s < 3600: return f"{s//60}m"
    if s < 86400: return f"{s//3600}h"
    return f"{s//86400}d"

# ============================================================
# 🔗 LINK CHECK
# ============================================================

LINK_RE = re.compile(r"(https?://|t\.me/|www\.)")

def is_link(text):
    return bool(text and LINK_RE.search(text))

# ============================================================
# 🧠 FILTER LOGIC
# ============================================================

def should_delete(msg: Message, mode):
    text = msg.text or msg.caption or ""

    if mode == "all":
        return True
    if mode == "media":
        return bool(msg.media)
    if mode == "links":
        return is_link(text)
    if mode == "text":
        return bool(text)
    if mode == "bots":
        return bool(msg.from_user and msg.from_user.is_bot)
    if mode == "commands":
        return text.startswith("/")

    return False

# ============================================================
# 🗑 DELETE TASK
# ============================================================

async def delete_later(client: Client, chat_id: int, msg_id: int, delay: int):
    task = asyncio.current_task()
    pending_tasks.add(task)

    try:
        await asyncio.sleep(delay)

        try:
            await client.delete_messages(chat_id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.delete_messages(chat_id, msg_id)
        except:
            pass

    finally:
        pending_tasks.discard(task)

# ============================================================
# 👑 ADMIN CHECK
# ============================================================

async def is_admin(client: Client, msg: Message):
    if not msg.from_user:
        return False
    try:
        member = await client.get_chat_member(msg.chat.id, msg.from_user.id)
        return member.status in ("administrator", "creator")
    except:
        return False

# ============================================================
# ⚙ COMMAND HANDLER
# ============================================================

async def autodel_cmd(client: Client, msg: Message):

    if not await is_admin(client, msg):
        return await msg.reply("❌ Admin only")

    cid = msg.chat.id
    parts = msg.text.split()

    # 📊 STATUS
    if len(parts) == 1:
        delay = auto_delete_chats.get(cid)
        mode = auto_delete_modes.get(cid, "all")

        if delay:
            return await msg.reply(
                f"""
⚙️ <b>AUTO DELETE STATUS</b>

🟢 Status: ENABLED
⏱ Delay: <code>{format_time(delay)}</code>
🎯 Mode: <code>{mode}</code>
""",
                parse_mode=ParseMode.HTML
            )
        return await msg.reply("🔴 AutoDelete is OFF")

    # ❌ OFF
    if parts[1].lower() in ("off", "disable"):
        auto_delete_chats.pop(cid, None)
        auto_delete_modes.pop(cid, None)
        return await msg.reply("🔴 AutoDelete Disabled")

    # ⚙ SET
    if len(parts) < 3:
        return await msg.reply(
            "❌ Use: /autodel 30s all/media/links/text/bots/commands"
        )

    delay = parse_time(parts[1])
    mode = parts[2].lower()

    valid_modes = ["all", "media", "links", "text", "bots", "commands"]

    if delay is None or mode not in valid_modes:
        return await msg.reply("❌ Invalid format or mode")

    auto_delete_chats[cid] = delay
    auto_delete_modes[cid] = mode

    await msg.reply(
        f"""
🟢 <b>AUTO DELETE ENABLED</b>

⏱ Delay: <code>{format_time(delay)}</code>
🎯 Mode: <code>{mode}</code>

⚡ Messages will be auto removed.
""",
        parse_mode=ParseMode.HTML
    )

# ============================================================
# 👀 MESSAGE WATCHER
# ============================================================

async def watcher(client: Client, msg: Message):

    cid = msg.chat.id

    if cid not in auto_delete_chats:
        return

    if not msg.from_user or msg.from_user.is_self:
        return

    delay = auto_delete_chats[cid]
    mode = auto_delete_modes.get(cid, "all")

    if should_delete(msg, mode):
        asyncio.create_task(
            delete_later(client, cid, msg.id, delay)
        )

# ============================================================
# ✏️ EDITED MESSAGE DELETE
# ============================================================

async def edited_watcher(client: Client, msg: Message):

    cid = msg.chat.id

    if cid not in auto_delete_chats:
        return

    if not msg.from_user or msg.from_user.is_self:
        return

    try:
        await msg.delete()
    except:
        pass

# ============================================================
# 🚀 REGISTER
# ============================================================

def register_autodel(app: Client):

    app.add_handler(
        filters.command("autodel") & filters.group,
        autodel_cmd
    )

    app.add_handler(
        filters.group & ~filters.service,
        watcher
    )

    app.add_handler(
        filters.edited & filters.group,
        edited_watcher
    )

    print("🚀 AutoDelete + EditDelete PRO MAX Loaded")
