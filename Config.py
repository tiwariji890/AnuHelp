# ============================================================
# 🤖 Group Manager Bot - FULL CONFIG FILE (FINAL PRO)
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 🔑 BOT CREDENTIALS (IMPORTANT)
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
# 👑 DEV / APPROVAL SYSTEM (NEW 🔥)
# ============================================================

# Multiple dev IDs (space separated in .env)
DEV_LIST = list(map(int, os.getenv("DEV_LIST", str(OWNER_ID)).split()))

# Auto approve admins
AUTO_APPROVE_ADMINS = os.getenv("AUTO_APPROVE_ADMINS", "True") == "True"

# Devs always bypass everything
IGNORE_DEVS = os.getenv("IGNORE_DEVS", "True") == "True"

# ============================================================
# 📢 CHANNEL / SUPPORT
# ============================================================

SUPPORT_CHAT = int(os.getenv("SUPPORT_CHAT", "-1001234567890"))
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/+xxxx")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "https://t.me/xxxx")

# ============================================================
# 🖼️ START MESSAGE IMAGE
# ============================================================

START_IMAGE = os.getenv(
    "START_IMAGE",
    "https://files.catbox.moe/9sqgv0.jpg"
)

# ============================================================
# 💬 SUPPORT SYSTEM CONFIG
# ============================================================

SUPPORT_COOLDOWN = int(os.getenv("SUPPORT_COOLDOWN", "30"))

# ============================================================
# 🚫 ABUSE FILTER CONFIG
# ============================================================

ABUSE_ENABLED = os.getenv("ABUSE_ENABLED", "True") == "True"
ABUSE_SKIP_ADMINS = os.getenv("ABUSE_SKIP_ADMINS", "False") == "True"
ABUSE_WARN_LIMIT = int(os.getenv("ABUSE_WARN_LIMIT", "3"))
ABUSE_MUTE_TIME = int(os.getenv("ABUSE_MUTE_TIME", "10"))

# ============================================================
# ⚠️ WARN SYSTEM
# ============================================================

MAX_WARNS = int(os.getenv("MAX_WARNS", "3"))

# ============================================================
# 📊 LOGGING
# ============================================================

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))

# ============================================================
# 🔒 SECURITY
# ============================================================

IGNORE_ADMINS = os.getenv("IGNORE_ADMINS", "False") == "True"

# ============================================================
# ⚙️ OTHER SETTINGS
# ============================================================

AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
DEBUG = os.getenv("DEBUG", "True") == "True"

# ============================================================
# ✅ VALIDATION (IMPORTANT)
# ============================================================

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("❌ API_ID, API_HASH, BOT_TOKEN required!")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI required!")

if not OWNER_ID:
    print("⚠️ OWNER_ID not set (recommended)")
