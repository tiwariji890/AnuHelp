def register_admin_panel(app):

    from pyrogram import filters
    from pyrogram.types import (
        InlineKeyboardMarkup,
        InlineKeyboardButton
    )
    from pyrogram.enums import ChatMemberStatus

    async def is_admin(client, chat_id, user_id):
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]

    # =========================
    # ADMIN PANEL COMMAND
    # =========================
    @app.on_message(filters.command("admin") & filters.group)
    async def admin_panel(client, message):
        if not await is_admin(client, message.chat.id, message.from_user.id):
            return await message.reply_text("❌ Only admins can open this panel.")

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔨 Ban", callback_data="admin_ban"),
                InlineKeyboardButton("🔇 Mute", callback_data="admin_mute")
            ],
            [
                InlineKeyboardButton("⚠️ Warn", callback_data="admin_warn"),
                InlineKeyboardButton("👮 Promote", callback_data="admin_promote")
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="admin_close")
            ]
        ])

        await message.reply_text(
            "⚙️ **Admin Panel**\nChoose action:",
            reply_markup=keyboard
        )

    # =========================
    # CALLBACK
    # =========================
    @app.on_callback_query(filters.regex("^admin_"))
    async def admin_callbacks(client, query):

        if not await is_admin(client, query.message.chat.id, query.from_user.id):
            return await query.answer("❌ Not admin", show_alert=True)

        data = query.data

        if data == "admin_ban":
            await query.message.edit_text("Reply user with /ban reason")

        elif data == "admin_mute":
            await query.message.edit_text("Reply user with /mute 10m")

        elif data == "admin_warn":
            await query.message.edit_text("Reply user with /warn reason")

        elif data == "admin_promote":
            await query.message.edit_text("Reply user with /promote")

        elif data == "admin_close":
            await query.message.delete()

        await query.answer()
