# ============================================================
# 🚨 POWERFUL ANTI RAID SYSTEM (ULTIMATE VERSION)
# ============================================================

import re
from datetime import datetime, timedelta, timezone

from pyrogram import filters
from pyrogram.types import Message

from utils.db import (
    get_antiraid_config,
    enable_antiraid,
    disable_antiraid,
    set_raid_time,
    set_ban_time,
    set_auto_trigger
)

from config import DEV_LIST
from app import pbot


# ============================================================
# 🧠 MEMORY TRACKER (SAFE)
# ============================================================
join_tracker = {}


# ============================================================
# ⏱ TIME PARSER (FIXED)
# ============================================================
def parse_time(text: str) -> int:
    match = re.fullmatch(r"(\d+)([hms])", text.lower())
    if not match:
        return 0

    val, unit = match.groups()
    val = int(val)

    if unit == "h":
        return val * 3600
    elif unit == "m":
        return val * 60
    elif unit == "s":
        return val


def human_time(seconds: int) -> str:
    return str(timedelta(seconds=seconds))


# ============================================================
# 👮 ADMIN CHECK
# ============================================================
async def is_admin(chat_id, user_id):
    if user_id in DEV_LIST:
        return True
    try:
        member = await pbot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False


# ============================================================
# 🚨 COMMANDS
# ============================================================

# ON / OFF / STATUS
@pbot.on_message(filters.command("antiraid") & filters.group)
async def antiraid(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply("❌ Admin only")

    args = m.text.split()

    if len(args) == 1:
        cfg = await get_antiraid_config(m.chat.id)
        if cfg.get("enabled_until"):
            return await m.reply("🛡 AntiRaid ACTIVE")
        return await m.reply("❌ AntiRaid OFF")

    if args[1] == "off":
        await disable_antiraid(m.chat.id)
        return await m.reply("✅ AntiRaid Disabled")

    sec = parse_time(args[1])
    if not sec:
        return await m.reply("❌ Use format like 10m / 1h")

    until = datetime.now(timezone.utc) + timedelta(seconds=sec)
    await enable_antiraid(m.chat.id, until)

    await m.reply(f"🚨 AntiRaid Enabled for {human_time(sec)}")


# AUTO TRIGGER
@pbot.on_message(filters.command("autoantiraid") & filters.group)
async def auto_antiraid(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return

    args = m.text.split()

    if len(args) < 2:
        return await m.reply("Usage: /autoantiraid 5")

    if args[1] == "off":
        await set_auto_trigger(m.chat.id, 0)
        return await m.reply("❌ Auto AntiRaid OFF")

    try:
        val = int(args[1])
    except:
        return await m.reply("❌ Invalid number")

    await set_auto_trigger(m.chat.id, val)
    await m.reply(f"✅ Auto Trigger = {val} joins/min")


# RAID TIME
@pbot.on_message(filters.command("raidtime") & filters.group)
async def raid_time_cmd(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply("❌ Admin only")

    args = m.text.split()

    if len(args) < 2:
        return await m.reply("Usage: /raidtime 10m")

    sec = parse_time(args[1])
    if not sec:
        return await m.reply("❌ Invalid time")

    await set_raid_time(m.chat.id, sec)
    await m.reply(f"⏱ Raid Time = {human_time(sec)}")


# BAN TIME
@pbot.on_message(filters.command("bantime") & filters.group)
async def ban_time_cmd(_, m: Message):
    if not await is_admin(m.chat.id, m.from_user.id):
        return await m.reply("❌ Admin only")

    args = m.text.split()

    if len(args) < 2:
        return await m.reply("Usage: /bantime 30m")

    sec = parse_time(args[1])
    if not sec:
        return await m.reply("❌ Invalid time")

    await set_ban_time(m.chat.id, sec)
    await m.reply(f"🚫 Ban Time = {human_time(sec)}")


# ============================================================
# 🚨 MAIN RAID DETECTION SYSTEM
# ============================================================

@pbot.on_message(filters.new_chat_members)
async def anti_raid_join(_, m: Message):
    chat_id = m.chat.id
    now = datetime.now(timezone.utc)

    cfg = await get_antiraid_config(chat_id)

    # Track joins
    join_tracker.setdefault(chat_id, [])
    join_tracker[chat_id].append(now)

    # Keep last 60 sec only
    join_tracker[chat_id] = [
        t for t in join_tracker[chat_id]
        if (now - t).total_seconds() < 60
    ]

    # =========================
    # ⚡ AUTO TRIGGER
    # =========================
    trigger = cfg.get("auto_trigger", 0)

    if trigger and len(join_tracker[chat_id]) >= trigger:
        raid_time = cfg.get("raid_time", 21600)

        until = now + timedelta(seconds=raid_time)
        await enable_antiraid(chat_id, until)

        await m.reply("🚨 AUTO ANTIRAID ACTIVATED!")

    # =========================
    # 🛡 ACTIVE PROTECTION
    # =========================
    if cfg.get("enabled_until") and cfg["enabled_until"] > now:

        ban_time = cfg.get("ban_time", 3600)
        banned = []

        for user in m.new_chat_members:
            try:
                # Ignore admins
                member = await pbot.get_chat_member(chat_id, user.id)
                if member.status in ["administrator", "creator"]:
                    continue

                await pbot.ban_chat_member(
                    chat_id,
                    user.id,
                    until_date=now + timedelta(seconds=ban_time)
                )

                banned.append(user.first_name)

            except:
                pass

        if banned:
            await m.reply(
                f"🚫 RAID MODE ACTIVE!\n\n"
                f"👤 Banned: {', '.join(banned)}"
            )
