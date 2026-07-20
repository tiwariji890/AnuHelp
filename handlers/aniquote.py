# ============================================================
# 📝 ANI-QUOTE SYSTEM (PYROGRAM VERSION - STABLE)
# ============================================================

import re
import os
import html
import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

# ============================================================
# MODULE INFO
# ============================================================

__MODULE__ = "𝐀ɴɪ-𝐐ᴜᴏᴛᴇ📝"

__HELP__ = """
*𝐀ɴɪ-𝐐ᴜᴏᴛᴇ📝*

*Description:*  
Search anime quotes by character or get random quotes.

*Commands:*  
❂ /aniquote — Random quote  
❂ /aniquote naruto — Search  
❂ /aniquote luffy page 2 — Page
"""


# ============================================================
# 🔥 MAIN FUNCTION REGISTER
# ============================================================

def register_aniquote(app):

    @app.on_message(filters.command("aniquote") & filters.group)
    async def aniquote_handler(client, message: Message):

        m = message

        # =========================
        # PARSE INPUT
        # =========================
        search = None
        page = 1

        if len(m.command) > 1:
            search = " ".join(m.command[1:])

            page_match = re.search(r'page\s+(\d+)', search, re.IGNORECASE)
            if page_match:
                page = int(page_match.group(1))
                search = re.sub(r'page\s+\d+', '', search, flags=re.IGNORECASE).strip()

        random = False if search else True

        # =========================
        # LOADING MESSAGE
        # =========================
        status = await m.reply_text("🎧 Fetching Anime Quotes...")

        # =========================
        # FETCH DATA (API)
        # =========================
        url = "https://animechan.xyz/api/random" if random else f"https://animechan.xyz/api/quotes?character={search}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return await status.edit("❌ API Error")

                    data = await resp.json()

        except Exception as e:
            return await status.edit(f"❌ Error:\n`{e}`")

        # =========================
        # NORMALIZE DATA
        # =========================
        if random:
            data = [data]

        if not data:
            return await status.edit("❌ No results found.")

        # =========================
        # LIMIT (ANTI SPAM)
        # =========================
        data = data[:5]  # max 5 quotes

        # =========================
        # SEND QUOTES
        # =========================
        for q in data:
            quote = html.escape(q.get("quote", "No quote"))
            character = html.escape(q.get("character", "Unknown"))
            anime = html.escape(q.get("anime", "Unknown"))

            text = f"""
<blockquote>{quote}</blockquote>
<b>Character:</b> <code>{character}</code>
<b>Anime:</b> <code>{anime}</code>
""".strip()

            await m.reply_text(text, parse_mode=ParseMode.HTML)

        # =========================
        # DONE
        # =========================
        await status.edit("✅ Quotes Sent Successfully")
