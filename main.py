# ============================================================
# 🤖 Group Manager Bot - Main Entry (ULTRA PRO MAX FINAL)
# ============================================================

import logging
import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

# 🔐 Security
from security import verify_integrity, get_runtime_key

# 📦 Handlers
from handlers import register_all_handlers

# 🗄️ DB
from db import create_indexes


# ============================================================
# ⚙️ Logging Setup
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger("MAIN")

logger.info("🚀 Starting Group Manager Bot...")


# ============================================================
# 🔐 Security Check
# ============================================================

try:
    verify_integrity()
    RUNTIME_KEY = get_runtime_key()
    logger.info("🔐 Security check passed!")
except Exception as e:
    logger.error(f"❌ Security check failed: {e}")
    exit()


# ============================================================
# 🤖 Bot Client
# ============================================================

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,  # 🔥 boosted
    sleep_threshold=15
)


# ============================================================
# 🚀 STARTUP TASKS
# ============================================================

async def startup():
    logger.info("⚙️ Running startup tasks...")

    try:
        await create_indexes()
        logger.info("✅ Database indexes ready")
    except Exception as e:
        logger.error(f"❌ DB Index error: {e}")

    logger.info("🚀 Bot fully started!")


# ============================================================
# 🧹 CLEAN SHUTDOWN
# ============================================================

async def shutdown():
    logger.warning("🛑 Shutting down bot...")
    await app.stop()
    logger.info("✅ Bot stopped safely")


# ============================================================
# 📦 Register All Handlers
# ============================================================

try:
    register_all_handlers(app)
    logger.info("✅ All handlers loaded!")
except Exception as e:
    logger.error(f"❌ Handler error: {e}")
    exit()


# ============================================================
# ❤️ KEEP BOT ALIVE (SAFE FALLBACK)
# ============================================================

@app.on_message(filters.private & filters.text & filters.incoming)
async def alive_ping(client, message):
    return


# ============================================================
# ▶️ MAIN RUNNER (ANTI-CRASH LOOP)
# ============================================================

async def main():
    while True:
        try:
            await app.start()
            await startup()

            logger.info("🤖 Bot is running...")
            await idle()

        except Exception as e:
            logger.error(f"❌ Crash detected: {e}")
            logger.info("🔄 Restarting in 5 seconds...")
            await asyncio.sleep(5)

        finally:
            try:
                await shutdown()
            except:
                pass


# ============================================================
# ▶️ ENTRY POINT
# ============================================================

if __name__ == "__main__":
    from pyrogram import idle

    print("""
╔══════════════════════════════╗
║   🤖 GROUP MANAGER BOT      ║
║   🔥 ULTRA PRO MAX ACTIVE   ║
╚══════════════════════════════╝
""")

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.warning("⛔ Bot stopped manually")

    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
