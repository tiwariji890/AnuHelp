# ============================================================
# Group Manager Bot
# Author: Krishna-bots
)
# ============================================================

from pyrogram import filters
from pyrogram.types import Message

REPO_LINK = ""


def register_repo_handler(app):

    @app.on_message(filters.command("repo"))
    async def repo_handler(client, message: Message):

        await message.reply_text(
            f"📦 **Official Repository:**\n🔗 {REPO_LINK}",
            disable_web_page_preview=True
        )
