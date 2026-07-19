# ============================================================
# 🤖 Group Manager Bot - Main Entry (FINAL PRO VERSION)
# ============================================================

import logging
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# 🔐 Security
from security import verify_integrity, get_runtime_key

# 📦 Handlers
from handlers import register_all_handlers


# ============================================================
# ⚙️ Logging Setup
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("🚀 Starting Group Manager Bot...")


# ============================================================
# 🔐 Security Check
# ============================================================

try:
    verify_integrity()
    RUNTIME_KEY = get_runtime_key()
    logging.info("🔐 Security check passed!")
except Exception as e:
    logging.error(f"❌ Security check failed: {e}")
    exit()


# ============================================================
# 🤖 Bot Client
# ============================================================

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=10,
    sleep_threshold=10
)


# ============================================================
# 📦 Register All Handlers
# ============================================================

try:
    register_all_handlers(app)
    logging.info("✅ All handlers loaded!")
except Exception as e:
    logging.error(f"❌ Handler error: {e}")
    exit()


# ============================================================
# ❤️ KEEP BOT ALIVE (SAFE VERSION)
# ============================================================

# ⚠️ IMPORTANT:
# Ye handler sirf empty fallback hai
# Ye help system ko block nahi karega

@app.on_message(filters.private & filters.text & filters.incoming)
async def alive_ping(client, message):
    # agar kisi handler ne handle nahi kiya tab ye chalega
    return


# ============================================================
# ▶️ START BOT
# ============================================================

if __name__ == "__main__":
    try:
        print("""
╔══════════════════════════════╗
║   🤖 GROUP MANAGER BOT      ║
║   🔥 ALL SYSTEMS ACTIVE     ║
╚══════════════════════════════╝
""")

        app.run()

    except KeyboardInterrupt:
        logging.warning("⛔ Bot stopped manually")

    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")
