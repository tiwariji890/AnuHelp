import re
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from datetime import datetime, timedelta

from database import (
    add_warn, get_warn_limit, add_log, get_admins,
    get_global_abuse, get_group_abuse,
    add_group_abuse, remove_group_abuse
)

# ==========================================================
# 🔥 DEFAULT ABUSE WORD LIST
# ==========================================================

ABUSE_WORDS = [
    "madarchod", "bhenchod", "gandu", "chutiya", "randi",
    "mc", "bc", "bsdk", "lund", "chodu",
    "fuck", "bitch", "asshole", "bastard", "dick",
    "harami", "kamina", "kuttiya", "gand"
]

# ==========================================================
# 🧠 INTELLIGENT NORMALIZER
# ==========================================================

def normalize_text(text: str) -> str:
    text = text.lower()

    # remove spaces
    text = re.sub(r"\s+", "", text)

    # replace symbols
    replacements = {
        "@": "a", "0": "o", "1": "i", "$": "s", "3": "e", "7": "t"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # remove repeated letters
    text = re.sub(r"(.)\1+", r"\1", text)

    return text


# ==========================================================
# 🛡️ ADMIN CHECK
# ==========================================================

async def is_admin(chat_id, user_id):
    admins = await get_admins(chat_id)
    return user_id in admins


# ==========================================================
# 🚨 MAIN ABUSE FILTER
# ==========================================================

@Client.on_message(filters.group & filters.text)
async def abuse_filter(client, message):
    if not message.text:
        return

    raw_text = message.text.lower()
    text = normalize_text(raw_text)

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Admin check (no bypass now)
    is_admin_user = await is_admin(chat_id, user_id)

    # Load DB words
    global_words = await get_global_abuse()
    group_words = await get_group_abuse(chat_id)

    ALL_WORDS = list(set(ABUSE_WORDS + global_words + group_words))

    abuse_regex = re.compile(
        r"\b(" + "|".join(map(re.escape, ALL_WORDS)) + r")\b",
        re.IGNORECASE
    )

    found = abuse_regex.search(raw_text) or abuse_regex.search(text)

    if not found:
        return

    # ❌ DELETE MESSAGE (everyone)
    try:
        await message.delete()
    except:
        pass

    # 🔥 ADMIN CASE
    if is_admin_user:
        await message.reply_text(
            f"⚠️ Admin {message.from_user.mention} abuse not allowed!",
            quote=True
        )
        return

    # =========================
    # 👤 NORMAL USER FLOW
    # =========================

    warn_count = await add_warn(chat_id, user_id)
    warn_limit = await get_warn_limit(chat_id)

    action = "⚠️ Warning"

    if warn_count >= warn_limit:
        try:
            await client.restrict_chat_member(
                chat_id,
                user_id,
                ChatPermissions(),
                until_date=datetime.now() + timedelta(minutes=10)
            )
            action = "🔇 Muted (10 min)"
        except:
            action = "❌ Mute Failed"

    await add_log(chat_id, action, user_id)

    await message.reply_text(
        f"""
╭─❖ 𝗔𝗕𝗨𝗦𝗘 𝗦𝗬𝗦𝗧𝗘𝗠 ❖─╮
│ 👤 User: {message.from_user.mention}
│ 📊 Warns: {warn_count}/{warn_limit}
│ ⚡ Action: {action}
╰────────────────────╯
""",
        quote=True
    )


# ==========================================================
# ⚙️ COMMAND: ADD GROUP ABUSE
# ==========================================================

@Client.on_message(filters.command("addabuse") & filters.group)
async def add_abuse_word(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: /addabuse word")

    word = message.command[1].lower()

    await add_group_abuse(message.chat.id, word)

    await message.reply(f"✅ Added:\n`{word}`")


# ==========================================================
# ⚙️ COMMAND: REMOVE GROUP ABUSE
# ==========================================================

@Client.on_message(filters.command("delabuse") & filters.group)
async def remove_abuse_word(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Usage: /delabuse word")

    word = message.command[1].lower()

    await remove_group_abuse(message.chat.id, word)

    await message.reply(f"❌ Removed:\n`{word}`")
  
