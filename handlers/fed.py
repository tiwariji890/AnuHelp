# ============================================================
# 🌐 FEDERATION SYSTEM (ULTRA PRO)
# ============================================================

from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID, DEV_LIST

# ============================================================
# 📦 STORAGE (Use Mongo later for permanent)
# ============================================================

FEDS = {}            # fed_id → {"name": str, "owner": id, "admins": []}
USER_FED = {}        # chat_id → fed_id
GBANNED = {}         # fed_id → set(user_ids)

# ============================================================
# 🧠 HELPERS
# ============================================================

def is_fed_admin(user_id, fed_id):
    fed = FEDS.get(fed_id)
    if not fed:
        return False
    return user_id == fed["owner"] or user_id in fed["admins"] or user_id in DEV_LIST


# ============================================================
# 🚀 REGISTER
# ============================================================

def register_fed_handlers(app):

    # =========================
    # 🆕 CREATE FED
    # =========================
    @app.on_message(filters.command("newfed") & filters.private)
    async def new_fed(client, message: Message):

        name = message.text.split(maxsplit=1)
        if len(name) < 2:
            return await message.reply_text("❌ Usage: /newfed FedName")

        fed_id = f"FED-{len(FEDS)+1}"
        FEDS[fed_id] = {
            "name": name[1],
            "owner": message.from_user.id,
            "admins": []
        }

        GBANNED[fed_id] = set()

        await message.reply_text(
            f"✅ **Federation Created**\n\n"
            f"🆔 `{fed_id}`\n📛 {name[1]}"
        )

    # =========================
    # 🔗 JOIN FED
    # =========================
    @app.on_message(filters.command("joinfed") & filters.group)
    async def join_fed(client, message: Message):

        args = message.text.split()
        if len(args) < 2:
            return await message.reply_text("❌ Usage: /joinfed FED-ID")

        fed_id = args[1]

        if fed_id not in FEDS:
            return await message.reply_text("❌ Invalid Fed ID")

        USER_FED[message.chat.id] = fed_id

        await message.reply_text(
            f"✅ Group joined federation `{fed_id}`"
        )

    # =========================
    # 🚪 LEAVE FED
    # =========================
    @app.on_message(filters.command("leavefed") & filters.group)
    async def leave_fed(client, message: Message):

        if message.chat.id not in USER_FED:
            return await message.reply_text("❌ Not in any federation")

        del USER_FED[message.chat.id]

        await message.reply_text("🚪 Left federation")

    # =========================
    # 🔨 GLOBAL BAN
    # =========================
    @app.on_message(filters.command("gban") & filters.group)
    async def gban_user(client, message: Message):

        if message.chat.id not in USER_FED:
            return await message.reply_text("❌ This group is not in a federation")

        fed_id = USER_FED[message.chat.id]

        if not is_fed_admin(message.from_user.id, fed_id):
            return

        if not message.reply_to_message:
            return await message.reply_text("❌ Reply to user")

        user_id = message.reply_to_message.from_user.id

        GBANNED[fed_id].add(user_id)

        await message.reply_text(
            f"🔨 **Globally Banned**\nUser: `{user_id}`"
        )

    # =========================
    # ♻️ UNGBAN
    # =========================
    @app.on_message(filters.command("ungban") & filters.group)
    async def ungban_user(client, message: Message):

        fed_id = USER_FED.get(message.chat.id)
        if not fed_id:
            return

        if not is_fed_admin(message.from_user.id, fed_id):
            return

        if not message.reply_to_message:
            return await message.reply_text("❌ Reply to user")

        user_id = message.reply_to_message.from_user.id

        GBANNED[fed_id].discard(user_id)

        await message.reply_text(
            f"♻️ **User Unbanned** `{user_id}`"
        )

    # =========================
    # 🚫 AUTO BAN ENFORCE
    # =========================
    @app.on_message(filters.group)
    async def enforce_gban(client, message: Message):

        fed_id = USER_FED.get(message.chat.id)
        if not fed_id:
            return

        user_id = message.from_user.id

        if user_id in GBANNED.get(fed_id, set()):
            try:
                await message.chat.ban_member(user_id)
                await message.reply_text("🚫 Globally banned user removed")
            except:
                pass

    # =========================
    # 📊 FED INFO
    # =========================
    @app.on_message(filters.command("fedinfo"))
    async def fed_info(client, message: Message):

        fed_id = None

        if message.chat.id in USER_FED:
            fed_id = USER_FED[message.chat.id]

        if not fed_id:
            return await message.reply_text("❌ Not in federation")

        fed = FEDS.get(fed_id)

        await message.reply_text(
            f"""
╔═══❰ 🌐 FED INFO ❱═══╗
🆔 `{fed_id}`
📛 {fed['name']}
👑 Owner: `{fed['owner']}`
👥 Admins: {len(fed['admins'])}
🚫 Gbanned: {len(GBANNED[fed_id])}
╚═══════════════════╝
"""
        )
