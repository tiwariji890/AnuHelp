# ============================================================
# 🤖 HANDLERS LOADER (ULTIMATE PRO MAX)
# ============================================================

import logging
import importlib
import time

# ============================================================
# 🎨 LOGGING SETUP (MODERN)
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ULTRA-BOT")

# ============================================================
# 🛡 SAFE IMPORT FUNCTION
# ============================================================

def safe_import(module_name: str, func_name: str):
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        return func
    except Exception as e:
        logger.warning(f"⚠️ {module_name} failed → {e}")
        return None

# ============================================================
# 📦 MODULE CONFIG (AUTO EXTENDABLE)
# ============================================================

MODULES = [
    # BASIC
    ("Start System", "handlers.start", "register_handlers"),
    ("Group Commands", "handlers.group_commands", "register_group_commands"),
    ("Repo System", "handlers.repo", "register_repo_handler"),

    # HELP
    ("Support System", "handlers.help_support", "register_help_handler"),

    # ADMIN
    ("Admin Panel", "handlers.adminpanel", "register_admin_panel"),

    # APPROVAL
    ("Approval System", "handlers.approve", "register_approval_handlers"),

    # SECURITY
    ("Anti-Spam", "handlers.auto_spam_detection", "register_auto_spam"),
    ("Abuse Filter", "handlers.abuse", "register_abuse_system"),

    # ANTIFLOOD
    ("AntiFlood Core", "handlers.antiflood", "register_antiflood"),
    ("AntiFlood Commands", "handlers.antiflood", "register_antiflood_commands"),

    # NSFW
    ("NSFW Filter", "handlers.nsfw", "register_nsfw_filter"),
    ("NSFW Commands", "handlers.nsfw_commands", "register_nsfw_commands"),

    # OTHER
    ("Anti-Edit", "handlers.antiedit", "register_antiedit"),
    ("Auto Clean", "handlers.intel", "register_autoclean"),
    ("AniQuote", "handlers.aniquote", "register_aniquote"),
]

# ============================================================
# 🚨 SPECIAL HANDLERS (DIRECT)
# ============================================================

SPECIAL_HANDLERS = [
    ("AntiRaid Core", "handlers.antiraid", "antiraid"),
    ("Auto AntiRaid", "handlers.antiraid", "auto_antiraid"),
    ("AntiRaid Join", "handlers.antiraid", "anti_raid_join"),
]

# ============================================================
# 🧠 MAIN LOADER FUNCTION
# ============================================================

def register_all_handlers(app):

    logger.info("🚀 Booting Ultra Bot System...\n")
    start_time = time.time()

    loaded = 0
    failed = 0

    # ========================================================
    # 🔄 LOAD NORMAL MODULES
    # ========================================================

    for name, module, func_name in MODULES:
        func = safe_import(module, func_name)

        if not func:
            logger.warning(f"⚠️ {name} skipped")
            failed += 1
            continue

        try:
            t1 = time.time()
            func(app)
            t2 = time.time()

            logger.info(f"✅ {name} ({round(t2 - t1, 3)}s)")
            loaded += 1

        except Exception as e:
            logger.error(f"❌ {name} crashed → {e}")
            failed += 1

    # ========================================================
    # 🚨 LOAD SPECIAL HANDLERS
    # ========================================================

    for name, module, handler_name in SPECIAL_HANDLERS:
        handler = safe_import(module, handler_name)

        if not handler:
            logger.warning(f"⚠️ {name} missing")
            failed += 1
            continue

        try:
            app.add_handler(handler)
            logger.info(f"🔥 {name}")
            loaded += 1

        except Exception as e:
            logger.error(f"❌ {name} error → {e}")
            failed += 1

    # ========================================================
    # 📊 FINAL REPORT
    # ========================================================

    total_time = round(time.time() - start_time, 2)

    logger.info("\n" + "=" * 40)
    logger.info("🚀 BOT LOADING COMPLETE")
    logger.info(f"✅ Loaded: {loaded}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"⏱ Time: {total_time}s")
    logger.info("=" * 40)
