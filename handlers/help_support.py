# ============================================================
# 💎 MODERN SUPPORT SYSTEM (PRO VERSION)
# ============================================================

from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from config import SUPPORT_CHAT, SUPPORT_COOLDOWN, ADMINS
import time
import random

# ============================================================
# 📦 STORAGE
# ============================================================

USER_MAP = {}       # msg_id → user_id
LAST_MSG = {}       # anti spam
TICKET_DB = {}      # ticket_id → user_id

# ============================================================
# 🎟️ GENERATE TICKET ID
# ============================================================

def generate_ticket():
    return f"TKT-{random.randint(1000, 9999)}"

# ============================================================
# 🧠 REGISTER HANDLER
# ============================================================

def register_help_handler(app):

    # ======================================================
    # 👤 USER → BOT (PRIVATE)
    # ======================================================
    @app.on_message(filters.private & ~filters.bot)
    async def forward_help(client, message: Message):

        user = message.from_user

        # 🚫 Anti-Spam
        now = time.time()
        last = LAST_MSG.get(user.id, 0)

        if now - last < SUPPORT_COOLDOWN:
            return await message.reply_text(
                "⏳ **Slow down!**\nSpam mat karo thoda wait karo."
            )

        LAST_MSG[user.id] = now

        if not (message.text or message.caption or message.media):
            return await message.reply_text("❌ Text ya media bhejo.")

        # 🎟️ Ticket ID
        ticket_id = generate_ticket()
        TICKET_DB[ticket_id] = user.id

        # 🧾 Stylish Message
        text = f"""
╔═══❰ 🎟️ SUPPORT TICKET ❱═══╗
┃ 🆔 Ticket: `{ticket_id}`
┃ 👤 User: {user.mention}
┃ 🆔 ID: `{user.id}`
┃
┃ 💬 Message:
┃ {message.text or message.caption or "📎 Media"}
╚════════════════════════╝
"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👤 Profile", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("❌ Close", callback_data=f"close_{ticket_id}")
            ]
        ])

        # 📤 SEND (ALL MEDIA SUPPORT)
        if message.media:
            fwd = await message.forward(SUPPORT_CHAT)

            info = await client.send_message(
                SUPPORT_CHAT,
                text,
                reply_markup=buttons
            )

            USER_MAP[fwd.id] = user.id
            USER_MAP[info.id] = user.id

        else:
            sent = await client.send_message(
                SUPPORT_CHAT,
                text,
                reply_markup=buttons
            )

            USER_MAP[sent.id] = user.id

        await message.reply_text(
            f"✅ **Ticket Created!**\n🎟️ ID: `{ticket_id}`\n⏳ Support reply ka wait karo."
        )

    # ======================================================
    # 🧑‍💻 ADMIN → USER (REPLY)
    # ======================================================
    @app.on_message(filters.reply & filters.chat(SUPPORT_CHAT))
    async def reply_help(client, message: Message):

        # 🔒 Only Admin
        if message.from_user.id not in ADMINS:
            return

        original = message.reply_to_message
        user_id = USER_MAP.get(original.id)

        if not user_id:
            return await message.reply_text("❌ User not found.")

        reply_text = f"""
╔═══❰ 💬 SUPPORT REPLY ❱═══╗
┃ 👨‍💻 Admin: {message.from_user.mention}
┃
┃ 💬 Reply:
┃ {message.text or message.caption or "📎 Media"}
╚════════════════════════╝
"""

        try:
            await client.send_chat_action(user_id, "typing")

            # 📤 SEND WITH MEDIA
            if message.media:
                await message.copy(user_id, caption=reply_text)
            else:
                await client.send_message(user_id, reply_text)

            await message.reply_text("✅ Reply sent.")

        except Exception as e:
            print(e)
            await message.reply_text("❌ User blocked bot.")

    # ======================================================
    # ❌ CLOSE TICKET
    # ======================================================
    @app.on_callback_query(filters.regex(r"close_(TKT-\d+)"))
    async def close_ticket(client, callback):

        ticket_id = callback.data.split("_")[1]
        user_id = TICKET_DB.get(ticket_id)

        await callback.message.edit_text(
            f"❌ Ticket `{ticket_id}` Closed"
        )

        if user_id:
            try:
                await client.send_message(
                    user_id,
                    f"❌ **Your ticket `{ticket_id}` has been closed.**"
                )
            except:
                pass

        await callback.answer("Closed ✅")
