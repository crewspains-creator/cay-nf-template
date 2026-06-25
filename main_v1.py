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
    "premium": 596,
    "standard": 409,
    "basic": 187,
    "prime": 59
}

def get_user_data(chat_id):
    if chat_id not in USER_DATA:
        USER_DATA[chat_id] = {
            "used": {"premium": 0, "standard": 0, "basic": 0, "prime": 0},
            "last_reset": datetime.now(),
            "lang": "en"
        }
    if datetime.now() - USER_DATA[chat_id]["last_reset"] > timedelta(hours=1):
        USER_DATA[chat_id]["used"] = {"premium": 0, "standard": 0, "basic": 0, "prime": 0}
        USER_DATA[chat_id]["last_reset"] = datetime.now()
    return USER_DATA[chat_id]

# ====================== KEYBOARDS ======================
def main_menu_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_netflix"), callback_data="netflix"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_prime"),   callback_data="prime")
    )
    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_status"),  callback_data="status"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_stock"),   callback_data="stock"),
        types.InlineKeyboardButton(languages.get_text(lang, "btn_help"),    callback_data="help")
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
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(languages.get_text(lang, "btn_prime_video", n=STOCK["prime"]), callback_data="tier_prime")
    )
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_by_country"), callback_data="by_country_prime"))
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

# ====================== BUILD FUNCTIONS ======================
def build_status(chat_id, lang="en"):
    user = get_user_data(chat_id)
    text = languages.get_text(lang, "status_title")
    tier_keys = [
        ("premium", "tier_premium"),
        ("standard", "tier_standard"),
        ("basic",   "tier_basic"),
        ("prime",   "tier_prime"),
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
        text += languages.get_text(
            lang, "status_tier",
            name=languages.get_text(lang, name_key),
            used=used, left=left, stock=stock, resets=resets_str
        )
    text += languages.get_text(lang, "status_footer")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_refresh"),   callback_data="status"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"), callback_data="main_menu"))
    return text, markup

def build_stock(lang="en"):
    text = languages.get_text(lang, "stock_title")
    for t, name_key in [
        ("premium",  "stock_premium"),
        ("standard", "stock_standard"),
        ("basic",    "stock_basic"),
        ("prime",    "stock_prime"),
    ]:
        text += languages.get_text(lang, "stock_row",
                                   name=languages.get_text(lang, name_key),
                                   count=STOCK[t])
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

# ====================== COMMANDS ======================
@bot.message_handler(commands=['start'])
def start_command(message):
    lang = get_lang(message.chat.id)
    bot.send_message(
        message.chat.id,
        languages.get_text(lang, "welcome"),
        reply_markup=main_menu_markup(lang),
        parse_mode="HTML"
    )

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
    lang = get_lang(message.chat.id)
    try:
        country = message.text.split(maxsplit=1)[1].upper()
        bot.reply_to(
            message,
            languages.get_text(lang, "country_searching", country=country),
            parse_mode="HTML"
        )
        time.sleep(2)
        bot.send_message(
            message.chat.id,
            languages.get_text(lang, "country_found", country=country),
            parse_mode="HTML"
        )
    except Exception:
        bot.reply_to(
            message,
            languages.get_text(lang, "country_usage"),
            parse_mode="HTML"
        )

# ====================== CALLBACKS ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user    = get_user_data(chat_id)
    lang    = user.get("lang", "en")
    data    = call.data

    if data == "main_menu":
        edit_current_message(call, languages.get_text(lang, "welcome"), main_menu_markup(lang))

    elif data == "netflix":
        edit_current_message(call, languages.get_text(lang, "choose_netflix"), netflix_tier_markup(lang))

    elif data == "prime":
        edit_current_message(call, languages.get_text(lang, "choose_prime"), prime_tier_markup(lang))

    elif data.startswith("tier_"):
        tier = data.split("_", 1)[1]

        if STOCK.get(tier, 0) <= 0:
            edit_current_message(call, languages.get_text(lang, "out_of_stock"))
            time.sleep(1.5)
            back  = prime_tier_markup(lang) if tier == "prime" else netflix_tier_markup(lang)
            label = "choose_prime"   if tier == "prime" else "choose_netflix"
            edit_current_message(call, languages.get_text(lang, label), back)
            return

        if user["used"].get(tier, 0) >= 3:
            edit_current_message(call, languages.get_text(lang, "hourly_limit"))
            time.sleep(1.5)
            back  = prime_tier_markup(lang) if tier == "prime" else netflix_tier_markup(lang)
            label = "choose_prime"   if tier == "prime" else "choose_netflix"
            edit_current_message(call, languages.get_text(lang, label), back)
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
        lang_code      = data.split("_", 1)[1]
        user["lang"]   = lang_code
        lang           = lang_code
        edit_current_message(call, languages.get_text(lang, "welcome"), main_menu_markup(lang))

    elif data in ("by_country_netflix", "by_country_prime"):
        edit_current_message(call, languages.get_text(lang, "country_usage"))

    bot.answer_callback_query(call.id)

# ====================== RUN ======================
if __name__ == "__main__":
    print("🚀 DEADFLIX Bot is running...")
    bot.set_my_commands([
        types.BotCommand("start",   "Open the main menu"),
        types.BotCommand("status",  "Check your usage limits"),
        types.BotCommand("stock",   "View available cookie stock"),
        types.BotCommand("country", "Get cookies for a specific country"),
        types.BotCommand("lang",    "Change language / Cambiar idioma"),
    ])
    bot.infinity_polling()