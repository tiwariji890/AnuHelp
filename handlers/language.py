# ============================================================
# 🌍 LANGUAGE SYSTEM (ULTRA PRO MAX FINAL)
# ============================================================

from googletrans import Translator
from db import db, cache_get, cache_set
from datetime import datetime

translator = Translator()

# ============================================================
# 🌍 90+ LANGUAGES
# ============================================================

LANGUAGES = {
    "en": "English", "hi": "Hindi", "bn": "Bengali", "te": "Telugu",
    "mr": "Marathi", "ta": "Tamil", "ur": "Urdu", "gu": "Gujarati",
    "kn": "Kannada", "ml": "Malayalam", "pa": "Punjabi", "or": "Odia",

    "fr": "French", "de": "German", "es": "Spanish", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)", "ja": "Japanese", "ko": "Korean",

    "ar": "Arabic", "fa": "Persian", "tr": "Turkish", "id": "Indonesian",
    "ms": "Malay", "th": "Thai", "vi": "Vietnamese",

    "nl": "Dutch", "sv": "Swedish", "no": "Norwegian", "da": "Danish",
    "fi": "Finnish", "pl": "Polish", "cs": "Czech", "sk": "Slovak",
    "hu": "Hungarian", "ro": "Romanian", "bg": "Bulgarian",
    "el": "Greek", "uk": "Ukrainian",

    "he": "Hebrew", "sw": "Swahili", "af": "Afrikaans",
    "sq": "Albanian", "hy": "Armenian", "az": "Azerbaijani",
    "eu": "Basque", "be": "Belarusian", "bs": "Bosnian",
    "ca": "Catalan", "hr": "Croatian", "eo": "Esperanto",
    "et": "Estonian", "gl": "Galician", "ka": "Georgian",
    "is": "Icelandic", "ga": "Irish", "la": "Latin",
    "lv": "Latvian", "lt": "Lithuanian", "mk": "Macedonian",
    "mt": "Maltese", "mn": "Mongolian", "ne": "Nepali",
    "sr": "Serbian", "sl": "Slovenian", "so": "Somali",
    "tl": "Filipino", "cy": "Welsh",

    "km": "Khmer", "lo": "Lao", "my": "Myanmar",
    "si": "Sinhala", "am": "Amharic", "zu": "Zulu"
}

# ============================================================
# 📦 SET GROUP LANGUAGE
# ============================================================

async def set_group_language(chat_id, lang_code):
    if lang_code not in LANGUAGES:
        return False

    await db.language.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "lang": lang_code,
            "enabled": True,
            "updated": datetime.utcnow()
        }},
        upsert=True
    )

    cache_set(f"lang:{chat_id}", lang_code)
    cache_set(f"lang_status:{chat_id}", True)
    return True


# ============================================================
# 🔘 ENABLE / DISABLE TRANSLATION
# ============================================================

async def toggle_language(chat_id, status: bool):
    await db.language.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

    cache_set(f"lang_status:{chat_id}", status)


async def is_language_enabled(chat_id):
    cached = cache_get(f"lang_status:{chat_id}")
    if cached is not None:
        return cached

    data = await db.language.find_one({"chat_id": chat_id})
    status = data.get("enabled", False) if data else False

    cache_set(f"lang_status:{chat_id}", status)
    return status


# ============================================================
# 📥 GET LANGUAGE
# ============================================================

async def get_group_language(chat_id):
    cached = cache_get(f"lang:{chat_id}")
    if cached:
        return cached

    data = await db.language.find_one({"chat_id": chat_id})
    lang = data.get("lang", "en") if data else "en"

    cache_set(f"lang:{chat_id}", lang)
    return lang


# ============================================================
# 🌍 TRANSLATE MESSAGE (OPTIMIZED)
# ============================================================

async def translate_text(chat_id, text):
    try:
        if not text or len(text) < 2:
            return text

        if not await is_language_enabled(chat_id):
            return text

        lang = await get_group_language(chat_id)

        if lang == "en":
            return text

        # 🚫 Avoid translating links / commands
        if text.startswith("/") or "http" in text:
            return text

        # ⚡ Prevent spam translations
        cache_key = f"translated:{chat_id}:{hash(text)}"
        cached = cache_get(cache_key)
        if cached:
            return cached

        translated = translator.translate(text, dest=lang)
        result = translated.text

        cache_set(cache_key, result)
        return result

    except Exception:
        return text
