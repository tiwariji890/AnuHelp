# ============================================================
# 🤖 Group Manager Bot - FULL CONFIG FILE (ULTRA PRO MAX FINAL)
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 🔑 BOT CREDENTIALS
# ============================================================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ============================================================
# 🗄️ DATABASE
# ============================================================

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "Cluster0")

# ============================================================
# 👑 OWNER / BOT INFO
# ============================================================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "Anu_helpbot")

# ============================================================
# 👑 DEV SYSTEM
# ============================================================

DEV_LIST = list(map(int, os.getenv("DEV_LIST", str(OWNER_ID)).split()))
AUTO_APPROVE_ADMINS = os.getenv("AUTO_APPROVE_ADMINS", "True") == "True"
IGNORE_DEVS = os.getenv("IGNORE_DEVS", "True") == "True"

# ============================================================
# 📢 CHANNEL / LOGS
# ============================================================

SUPPORT_CHAT = int(os.getenv("SUPPORT_CHAT", "-1001234567890"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))

# ============================================================
# ⚠️ WARN SYSTEM
# ============================================================

MAX_WARNS = int(os.getenv("MAX_WARNS", "3"))

# ============================================================
# 🔞 NSFW SYSTEM
# ============================================================

NSFW_DEFAULT = os.getenv("NSFW_DEFAULT", "False") == "True"

# ============================================================
# 🔐 CAPTCHA SYSTEM 🔥
# ============================================================

CAPTCHA_DEFAULT = os.getenv("CAPTCHA_DEFAULT", "True") == "True"
CAPTCHA_TIMEOUT = int(os.getenv("CAPTCHA_TIMEOUT", "120"))
CAPTCHA_MODE = os.getenv("CAPTCHA_MODE", "math")  # math / button

# ============================================================
# 🚫 ANTIBIOLINK SYSTEM 🔥
# ============================================================

ANTIBIOLINK_DEFAULT = os.getenv("ANTIBIOLINK_DEFAULT", "False") == "True"
ANTIBIOLINK_WARN_LIMIT = int(os.getenv("ANTIBIOLINK_WARN_LIMIT", "3"))
ANTIBIOLINK_MUTE_TIME = int(os.getenv("ANTIBIOLINK_MUTE_TIME", "600"))
ANTIBIOLINK_PUNISHMENT = os.getenv("ANTIBIOLINK_PUNISHMENT", "mute")  # mute / ban

ANTIBIOLINK_IGNORE_ADMINS = os.getenv("ANTIBIOLINK_IGNORE_ADMINS", "True") == "True"
ANTIBIOLINK_IGNORE_DEVS = os.getenv("ANTIBIOLINK_IGNORE_DEVS", "True") == "True"

ANTIBIOLINK_STRICT_MODE = os.getenv("ANTIBIOLINK_STRICT_MODE", "True") == "True"

WHITELIST_DOMAINS = os.getenv(
    "WHITELIST_DOMAINS",
    "t.me,telegram.me,youtube.com,youtu.be"
).split(",")

BIO_LINK_KEYWORDS = os.getenv(
    "BIO_LINK_KEYWORDS",
    "http,www,.com,.net,.org,t.me,telegram"
).split(",")

DELETE_ON_DETECT = os.getenv("DELETE_ON_DETECT", "True") == "True"
WARN_ON_DETECT = os.getenv("WARN_ON_DETECT", "True") == "True"

# ============================================================
# 🚨 ANTIRAID SYSTEM 🔥
# ============================================================

ANTIRAID_DEFAULT = os.getenv("ANTIRAID_DEFAULT", "False") == "True"
ANTIRAID_DURATION = int(os.getenv("ANTIRAID_DURATION", "600"))

# ============================================================
# 🔐 LOCK SYSTEM 🔥
# ============================================================

LOCK_TYPES = [
    "all", "photo", "video", "gif", "sticker",
    "link", "forward", "bots", "audio",
    "voice", "document", "poll"
]

# ============================================================
# 📌 PIN SYSTEM
# ============================================================

AUTO_PIN = os.getenv("AUTO_PIN", "False") == "True"

# ============================================================
# ⚡ PERFORMANCE / CACHE
# ============================================================

CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True") == "True"

# ============================================================
# 🔄 AUTO DELETE / CLEANUP
# ============================================================

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))

# ============================================================
# 🚀 SECURITY FLAGS
# ============================================================

STRICT_MODE = os.getenv("STRICT_MODE", "True") == "True"
IGNORE_PRIVATE = os.getenv("IGNORE_PRIVATE", "True") == "True"

# ============================================================
# 🌍 LANGUAGE SYSTEM 🔥 (NEW ADDED)
# ============================================================

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

AUTO_TRANSLATE = os.getenv("AUTO_TRANSLATE", "True") == "True"

TRANSLATE_MODE = os.getenv("TRANSLATE_MODE", "reply")  
# reply / replace / off

TRANSLATE_TIMEOUT = int(os.getenv("TRANSLATE_TIMEOUT", "5"))
TRANSLATE_RETRIES = int(os.getenv("TRANSLATE_RETRIES", "2"))

IGNORE_COMMANDS_IN_TRANSLATE = os.getenv(
    "IGNORE_COMMANDS_IN_TRANSLATE", "True"
) == "True"

# ============================================================
# ⚡ ADVANCED PERFORMANCE (FUTURE READY)
# ============================================================

CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

# ============================================================
# 🧠 DEBUG / LOGGING
# ============================================================

DEBUG = os.getenv("DEBUG", "True") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================================
# ❌ VALIDATION
# ============================================================

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ API_ID, API_HASH, BOT_TOKEN required!")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI required!")

print("✅ CONFIG LOADED SUCCESSFULLY 🚀")
