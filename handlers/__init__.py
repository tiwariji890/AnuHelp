# ============================================================
# 🤖 HANDLERS LOADER (SIMPLE + SAFE + POWERFUL)
# ============================================================

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BOT")

# ============================================================
# 📦 SAFE IMPORT
# ============================================================

def safe_import(module_name, func_name):
    try:
        module = __import__(module_name, fromlist=[func_name])
        return getattr(module, func_name)
    except Exception as e:
        logger.warning(f"⚠️ {module_name} not loaded: {e}")
        return None


# ============================================================
# 📂 IMPORT MODULES
# ============================================================

modules = {
    # BASIC
    "Start System": safe_import("handlers.start", "register_handlers"),
    "Group Commands": safe_import("handlers.group_commands", "register_group_commands"),
    "Repo System": safe_import("handlers.repo", "register_repo_handler"),

    # HELP
    "Support System": safe_import("handlers.help_support", "register_help_handler"),

    # ADMIN
    "Admin Panel": safe_import("handlers.adminpanel", "register_admin_panel"),

    # APPROVAL
    "Approval System": safe_import("handlers.approve", "register_approval_handlers"),

    # SECURITY
    "Anti-Spam": safe_import("handlers.auto_spam_detection", "register_auto_spam"),
    "Abuse Filter": safe_import("handlers.abuse", "register_abuse_system"),

    # ANTIFLOOD
    "AntiFlood": safe_import("handlers.antiflood", "register_antiflood"),
    "AntiFlood Commands": safe_import("handlers.antiflood", "register_antiflood_commands"),

    # NSFW
    "NSFW Filter": safe_import("handlers.nsfw", "register_nsfw_filter"),
    "NSFW Commands": safe_import("handlers.nsfw_commands", "register_nsfw_commands"),

    # OTHER
    "Anti-Edit": safe_import("handlers.antiedit", "register_antiedit"),
    "Auto Clean": safe_import("handlers.intel", "register_autoclean"),
    "AniQuote": safe_import("handlers.aniquote", "register_aniquote"),
}

# ANTIRAID (SPECIAL)
antiraid = safe_import("handlers.antiraid", "antiraid")
auto_antiraid = safe_import("handlers.antiraid", "auto_antiraid")
anti_raid_join = safe_import("handlers.antiraid", "anti_raid_join")


# ============================================================
# 🧠 REGISTER FUNCTION
# ============================================================

def register_all_handlers(app):

    logger.info("🚀 Loading Modules...\n")

    # NORMAL MODULES
    for name, func in modules.items():
        if func:
            try:
                func(app)
                logger.info(f"✅ {name}")
            except Exception as e:
                logger.error(f"❌ {name} error: {e}")
        else:
            logger.warning(f"⚠️ {name} missing")

    # ANTIRAID SPECIAL
    if antiraid:
        app.add_handler(antiraid)
        logger.info("✅ AntiRaid Core")

    if auto_antiraid:
        app.add_handler(auto_antiraid)
        logger.info("✅ Auto AntiRaid")

    if anti_raid_join:
        app.add_handler(anti_raid_join)
        logger.info("✅ AntiRaid Join")

    # FINAL LOG
    logger.info("🔥 BOT FULLY LOADED 🚀")
