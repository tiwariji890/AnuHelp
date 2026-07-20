# ============================================================
# 🤖 Group Manager Bot - FULL CONFIG FILE (FINAL PRO MAX)
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
# 📢 CHANNEL
# ============================================================

SUPPORT_CHAT = int(os.getenv("SUPPORT_CHAT", "-1001234567890"))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))

# ============================================================
# ⚠️ WARN SYSTEM
# ============================================================

MAX_WARNS = int(os.getenv("MAX_WARNS", "3"))

# ============================================================
# 🚫 ANTIBIOLINK SYSTEM 🔥
# ============================================================

ANTIBIOLINK_DEFAULT = os.getenv("ANTIBIOLINK_DEFAULT", "False") == "True"
ANTIBIOLINK_WARN_LIMIT = int(os.getenv("ANTIBIOLINK_WARN_LIMIT", "3"))
ANTIBIOLINK_MUTE_TIME = int(os.getenv("ANTIBIOLINK_MUTE_TIME", "600"))
ANTIBIOLINK_PUNISHMENT = os.getenv("ANTIBIOLINK_PUNISHMENT", "mute")

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
# ✅ VALIDATION
# ============================================================

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ API_ID, API_HASH, BOT_TOKEN required!")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI required!")
