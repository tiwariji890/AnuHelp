# ============================================================
# 🤖 ANTI-SPAM SYSTEM (MODERN + STYLISH + PRO)
# ============================================================

import re
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus, ParseMode

from db import add_warn, get_warn_limit, reset_warns, add_log


# ============================================================
# 🚫 SPAM KEYWORDS
# ============================================================

CONTEXT = [
    "crypto", "cash", "win", "bonus", "spins",
    "sell", "bet", "usdt", "profit", "invest",
    "reward", "money", "price", "promo",
    "nude", "porn", "sex", "airdrop",
    "referral", "earn", "buy", "fuck"
]

PATTERNS = [re.compile(rf"\b{p}\b", re.IGNORECASE) for p in CONTEXT]


# ============================================================
# 🔍 SPAM DETECTION
# ============================================================

async def check_spam(text: str):
    if not text:
        return False

    matched = [p.pattern.replace("\\b", "") for p in PATTERNS if p.search(text)]

    # 👇 More strict detection (>=2 keywords)
    return matched if len(matched) >= 2 else False


# ============================================================
# 🎭 CENSOR WORD
# ============================================================

def censor_word(word: str):
    return ''.join(c if i % 2 == 0 else '•' for i, c in enumerate(word))


# ============================================================
# 🎨 FORMAT USER
# ============================================================

def format_user(user):
    return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"


# ============================================================
# 🚀 REGISTER HANDLER
# ============================================================

def register_anti_spam(app):

    @app.on_message(filters.text & filters.group, group=-5)
    async def auto_spam_detect(client, message: Message):

        if not message.from_user:
            return

        user = message.from_user
        user_id = user.id
        chat_id = message.chat.id

        # =========================
        # 👑 ADMIN BYPASS
        # =========================
        try:
            member = await client.get_chat_member(chat_id, user_id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return
        except:
            return

        # =========================
        # 🧠 TEXT GET
        # =========================
        text = message.text or message.caption or ""
        result = await check_spam(text)

        if not result:
            return

        # =========================
        # ❌ DELETE MESSAGE
        # =========================
        try:
            await message.delete()
        except:
            pass

        # =========================
        # ⚠️ WARN SYSTEM
        # =========================
        warns = await add_warn(chat_id, user_id)
        limit = await get_warn_limit(chat_id)

        await add_log(chat_id, "spam", user_id)

        # =========================
        # 🔒 AUTO BAN
        # =========================
        if warns >= limit:
            try:
                await client.ban_chat_member(chat_id, user_id)
            except:
                pass

            await reset_warns(chat_id, user_id)

            return await message.reply_text(
                f"""
🚫 <b>USER BANNED</b>

👤 {format_user(user)}
📌 Reason: Spam Flood
⚠️ Limit: {limit}/{limit}

🛡️ Protection: Active
""",
                parse_mode=ParseMode.HTML
            )

        # =========================
        # 🎯 CENSOR KEYWORDS
        # =========================
        keywords = ", ".join([censor_word(k) for k in result])

        # =========================
        # ⚠️ WARNING MESSAGE
        # =========================
        await message.reply_text(
            f"""
⚠️ <b>SPAM DETECTED</b>

👤 {format_user(user)}
🔍 Keywords: <code>{keywords}</code>

📊 Warning: {warns}/{limit}
🛡️ Action: Message Deleted

❗ Avoid sending promotional or suspicious content.
""",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
