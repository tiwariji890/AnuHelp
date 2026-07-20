# ============================================================
# 👑 SUDO SYSTEM (ULTRA PRO MAX)
# ============================================================

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant

from config import OWNER_ID
from db import (
    add_sudo,
    remove_sudo,
    get_sudo_users,
    is_sudo_user
)

# ============================================================
# 🔐 FILTER
# ============================================================

def sudo_filter(_, __, message: Message):
    user_id = message.from_user.id
    return user_id == OWNER_ID or is_sudo_user(user_id)

sudo = filters.create(sudo_filter)


# ============================================================
# ➕ ADD SUDO
# ============================================================

async def add_sudo_cmd(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only Owner can add sudo users!")

    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to user to add sudo")

    user = message.reply_to_message.from_user

    if user.id == OWNER_ID:
        return await message.reply("⚠️ Owner is already supreme 😎")

    await add_sudo(user.id)

    await message.reply(
        f"✅ **Added to SUDO**\n👤 {user.mention}\n🆔 `{user.id}`"
    )


# ============================================================
# ➖ REMOVE SUDO
# ============================================================

async def remove_sudo_cmd(client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ Only Owner can remove sudo users!")

    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to user to remove sudo")

    user = message.reply_to_message.from_user

    if user.id == OWNER_ID:
        return await message.reply("❌ Cannot remove owner!")

    await remove_sudo(user.id)

    await message.reply(
        f"🚫 **Removed from SUDO**\n👤 {user.mention}"
    )


# ============================================================
# 📜 LIST SUDO USERS
# ============================================================

async def list_sudo_cmd(client, message: Message):
    sudo_users = await get_sudo_users()

    if not sudo_users:
        return await message.reply("❌ No sudo users set!")

    text = "👑 **SUDO USERS LIST**\n\n"

    for user_id in sudo_users:
        text += f"• `{user_id}`\n"

    await message.reply(text)


# ============================================================
# 🔍 CHECK SUDO
# ============================================================

async def check_sudo_cmd(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to user")

    user = message.reply_to_message.from_user

    if user.id == OWNER_ID:
        return await message.reply("👑 This is Owner")

    if await is_sudo_user(user.id):
        return await message.reply("✅ This user is SUDO")
    else:
        return await message.reply("❌ Not a sudo user")


# ============================================================
# 🚀 REGISTER HANDLERS
# ============================================================

def register(app):
    app.add_handler(
        filters.command("addsudo") & filters.private,
        add_sudo_cmd
    )

    app.add_handler(
        filters.command("delsudo") & filters.private,
        remove_sudo_cmd
    )

    app.add_handler(
        filters.command("sudolist") & filters.private,
        list_sudo_cmd
    )

    app.add_handler(
        filters.command("checksudo") & filters.private,
        check_sudo_cmd
  )
