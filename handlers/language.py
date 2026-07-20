# ============================================================
# 🌍 LANGUAGE SYSTEM (ULTRA PRO MAX)
# ============================================================

from googletrans import Translator
from db import db, cache_get, cache_set
from datetime import datetime

translator = Translator()

# ============================================================
# 🌍 90+ LANGUAGES
# ============================================================

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "te": "Telugu",
    "mr": "Marathi",
    "ta": "Tamil",
    "ur": "Urdu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "or": "Odia",

    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "ja": "Japanese",
    "ko": "Korean",

    "ar": "Arabic",
    "fa": "Persian",
    "tr": "Turkish",
    "id": "Indonesian",
    "ms": "Malay",
    "th": "Thai",
    "vi": "Vietnamese",

    "nl": "Dutch",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "fi": "Finnish",
    "pl": "Polish",
    "cs": "Czech",
    "sk": "Slovak",
    "hu": "Hungarian",
    "ro": "Romanian",
    "bg": "Bulgarian",
    "el": "Greek",
    "uk": "Ukrainian",

    "he": "Hebrew",
    "sw": "Swahili",
    "af": "Afrikaans",
    "sq": "Albanian",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bs": "Bosnian",
    "ca": "Catalan",
    "hr": "Croatian",
    "eo": "Esperanto",
    "et": "Estonian",
    "gl": "Galician",
    "ka": "Georgian",
    "is": "Icelandic",
    "ga": "Irish",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "mk": "Macedonian",
    "mt": "Maltese",
    "mn": "Mongolian",
    "ne": "Nepali",
    "sr": "Serbian",
    "sl": "Slovenian",
    "so": "Somali",
    "tl": "Filipino",
    "cy": "Welsh",

    # extra
    "km": "Khmer",
    "lo": "Lao",
    "my": "Myanmar",
    "si": "Sinhala",
    "am": "Amharic",
    "zu": "Zulu"
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
            "updated": datetime.utcnow()
        }},
        upsert=True
    )

    cache_set(f"lang:{chat_id}", lang_code)
    return True


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
# 🌍 TRANSLATE MESSAGE
# ============================================================

async def translate_text(chat_id, text):
    try:
        lang = await get_group_language(chat_id)

        if lang == "en":
            return text

        translated = translator.translate(text, dest=lang)
        return translated.text

    except Exception:
        return text
