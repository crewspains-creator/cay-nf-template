import telebot
from telebot import types
import time
import languages
from datetime import datetime, timedelta

# ====================== CONFIG ======================
TOKEN = "8863877477:AAEEW9DN1cP8GWkpiSENJA-56A1viiU28Yw"
bot = telebot.TeleBot(TOKEN)

USER_DATA = {}
STOCK = {
    "premium":     596,
    "standard":    409,
    "basic":       187,
    "prime":        59,
    "crunchyroll":   0,
    "spotify":       6
}

def get_user_data(chat_id):
    if chat_id not in USER_DATA:
        USER_DATA[chat_id] = {
            "used": {
                "premium": 0, "standard": 0, "basic": 0,
                "prime": 0, "crunchyroll": 0, "spotify": 0
            },
            "last_reset": datetime.now(),
            "lang": "en"
        }
    data = USER_DATA[chat_id]
    # Add missing keys for users already in memory
    for key in ("crunchyroll", "spotify"):
        if key not in data["used"]:
            data["used"][key] = 0
    if datetime.now() - data["last_reset"] > timedelta(hours=1):
        data["used"] = {
            "premium": 0, "standard": 0, "basic": 0,
            "prime": 0, "crunchyroll": 0, "spotify": 0
        }
        data["last_reset"] = datetime.now()
    return data

# ====================== KEYBOARDS ======================
def main_menu_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🎬 Netflix",     callback_data="netflix"),
        types.InlineKeyboardButton("🍿 Prime Video", callback_data="prime")
    )
    markup.add(
        types.InlineKeyboardButton("🦊 Crunchyroll", callback_data="crunchyroll"),
        types.InlineKeyboardButton("🎵 Spotify",     callback_data="spotify")
    )
    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_status"),   callback_data="status"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_stock"),    callback_data="stock"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_help"),     callback_data="help")
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
    markup.add(
        types.InlineKeyboardButton(f"🎬 Netflix ({country})",     callback_data=f"country_netflix_{country}"),
        types.InlineKeyboardButton(f"🍿 Prime Video ({country})", callback_data=f"country_prime_{country}")
    )
    markup.add(
        types.InlineKeyboardButton(f"🦊 Crunchyroll ({country})", callback_data=f"country_crunchyroll_{country}"),
        types.InlineKeyboardButton(f"🎵 Spotify ({country})",     callback_data=f"country_spotify_{country}")
    )
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

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
    text += f"  ├ 📛 Name: <code>{name}</code>\n"
    text += f"  ├ 🆔 User ID: <code>{chat_id}</code>\n"
    text += f"  ├ 🌐 Language: <code>{lang_name}</code>\n"
    text += f"  └ 🏅 Status: <code>{languages.get_text(lang, 'home_active')}</code>\n\n"
    text += languages.get_text(lang, "home_live_line") + "\n\n"
    text += languages.get_text(lang, "home_rules_header") + "\n"
    text += "  • 📈 " + languages.get_text(lang, "home_rule1") + "\n"
    text += "  • 🔄 " + languages.get_text(lang, "home_rule2") + "\n"
    text += "  • ❌ " + languages.get_text(lang, "home_rule3") + "\n\n"
    text += languages.get_text(lang, "home_status_hdr") + "\n"
    text += "──────────────────────"

    tiers = [
        ("premium",     "🔥 PREMIUM TIER"),
        ("standard",    "⭐ STANDARD TIER"),
        ("basic",       "🎯 BASIC TIER"),
        ("prime",       "🍿 PRIME VIDEO TIER"),
        ("crunchyroll", "🦊 CRUNCHYROLL TIER"),
        ("spotify",     "🎵 SPOTIFY TIER"),
    ]
    for t, label in tiers:
        used  = user["used"].get(t, 0)
        stock = STOCK.get(t, 0)
        reset_at = user["last_reset"] + timedelta(hours=1)
        now = datetime.now()
        if used > 0 and now < reset_at:
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

        bar = "🟩" * used + "⬜" * (3 - used)

        text += f"\n<b>{label}</b>\n"
        text += f"  ├ 📦 Stock: {stock_str}\n"
        text += f"  ├ 📈 Usage: {used}/3 [{bar}]\n"
        text += f"  └ 🔄 Reset: {resets_str}\n"

    text += "\n" + languages.get_text(lang, "home_choose")
    return text, main_menu_markup(lang)

def build_status(chat_id, lang="en"):
    user = get_user_data(chat_id)
    text = languages.get_text(lang, "status_title")
    tier_keys = [
        ("premium",     "tier_premium"),
        ("standard",    "tier_standard"),
        ("basic",       "tier_basic"),
        ("prime",       "tier_prime"),
        ("crunchyroll", "🦊 CRUNCHYROLL TIER"),
        ("spotify",     "🎵 SPOTIFY TIER"),
    ]
    for t, name_key in tier_keys:
        used  = user["used"].get(t, 0)
        left  = max(0, 3 - used)
        stock = STOCK.get(t, 0)
        reset_at = user["last_reset"] + timedelta(hours=1)
        now = datetime.now()
        if used > 0 and now < reset_at:
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
    items = [
        ("premium",     "🔥 PREMIUM"),
        ("standard",    "⭐ STANDARD"),
        ("basic",       "🎯 BASIC"),
        ("prime",       "🍿 PRIME VIDEO"),
        ("crunchyroll", "🦊 CRUNCHYROLL"),
        ("spotify",     "🎵 SPOTIFY"),
    ]
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

    elif data.startswith("tier_"):
        tier = data.split("_", 1)[1]
        back_markup, back_label = get_back_markup(tier, lang)

        if STOCK.get(tier, 0) <= 0:
            edit_current_message(call, languages.get_text(lang, "out_of_stock"))
            time.sleep(1.5)
            # back_label is either a lang key string or a raw HTML string
            if back_label.startswith("choose_"):
                label_text = languages.get_text(lang, back_label)
            else:
                label_text = back_label
            edit_current_message(call, label_text, back_markup)
            return

        if user["used"].get(tier, 0) >= 3:
            edit_current_message(call, languages.get_text(lang, "hourly_limit"))
            time.sleep(1.5)
            if back_label.startswith("choose_"):
                label_text = languages.get_text(lang, back_label)
            else:
                label_text = back_label
            edit_current_message(call, label_text, back_markup)
            return

        user["used"][tier] += 1
        STOCK[tier] = max(0, STOCK[tier] - 1)
        url = f"https://example.com/nftoken/{tier}-{int(time.time())}"
        delivery_text = languages.get_text(lang, "cookie_delivered", tier=tier.upper(), url=url)
        edit_current_message(call, delivery_text, main_menu_markup(lang))

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
    print("🚀 DEADFLIX Bot is running...")
    bot.delete_webhook(drop_pending_updates=True)
    bot.get_updates(offset=-1)
    bot.set_my_commands([
        types.BotCommand("start",   "Open the main menu"),
        types.BotCommand("status",  "Check your usage limits"),
        types.BotCommand("stock",   "View available cookie stock"),
        types.BotCommand("country", "Get cookies for a specific country"),
        types.BotCommand("lang",    "Change language / Cambiar idioma"),
    ])
    bot.infinity_polling()