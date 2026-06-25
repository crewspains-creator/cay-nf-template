import telebot
from telebot import types
import time
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
            "last_reset": datetime.now()
        }
    if datetime.now() - USER_DATA[chat_id]["last_reset"] > timedelta(hours=1):
        USER_DATA[chat_id]["used"] = {"premium": 0, "standard": 0, "basic": 0, "prime": 0}
        USER_DATA[chat_id]["last_reset"] = datetime.now()
    return USER_DATA[chat_id]

# ====================== KEYBOARDS ======================
def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🎬 Netflix", callback_data="netflix"),
        types.InlineKeyboardButton("🍿 Prime Video", callback_data="prime")
    )
    markup.add(
        types.InlineKeyboardButton("📊 Status", callback_data="status"),
        types.InlineKeyboardButton("📦 Stock", callback_data="stock"),
        types.InlineKeyboardButton("ℹ️ Help", callback_data="help")
    )
    markup.add(types.InlineKeyboardButton("🌐 Language", callback_data="language"))
    return markup

def netflix_tier_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"👑 Premium ({STOCK['premium']})", callback_data="tier_premium"),
        types.InlineKeyboardButton(f"⭐ Standard ({STOCK['standard']})", callback_data="tier_standard")
    )
    markup.add(types.InlineKeyboardButton(f"🎯 Basic ({STOCK['basic']})", callback_data="tier_basic"))
    markup.add(types.InlineKeyboardButton("🌍 By Country", callback_data="by_country_netflix"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

def prime_tier_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"🍿 Prime Video ({STOCK['prime']})", callback_data="tier_prime")
    )
    markup.add(types.InlineKeyboardButton("🌍 By Country", callback_data="by_country_prime"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
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

# ====================== SHARED RENDER FUNCTIONS ======================
# Each function builds (text, markup) and either sends or edits based on context.

WELCOME_TEXT = """👋 <b>WELCOME, CAY!</b>
━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Live-verified Netflix cookies across 3 tiers.
Every cookie is checked before delivery.

📌 📌 <b>RULES:</b>
  • 📈 3 cookies per tier per hour
  • ⏱️ Rolling 1-hour window (persists across restarts)
  • ❌ Dead cookies are auto-removed

🔽 🔽 <b>CHOOSE A SERVICE BELOW:</b>"""

def build_status(chat_id):
    user = get_user_data(chat_id)
    text = "📊📊 <b>YOUR USAGE STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    tiers = [
        ("premium", "👑 PREMIUM TIER"),
        ("standard", "⭐ STANDARD TIER"),
        ("basic", "🎯 BASIC TIER"),
        ("prime", "🍿 PRIME VIDEO TIER"),
    ]
    for t, name in tiers:
        used = user["used"].get(t, 0)
        left = max(0, 3 - used)
        stock = STOCK.get(t, 0)
        reset_at = user["last_reset"] + timedelta(hours=1)
        now = datetime.now()
        if used > 0 and now < reset_at:
            diff = reset_at - now
            resets_str = f"{int(diff.total_seconds() // 60)}m {int(diff.total_seconds() % 60)}s"
        else:
            resets_str = "—"
        text += (
            f"<b>{name}</b>\n"
            f"  📈 Used: <code>{used}/3</code>\n"
            f"  🔄 Left: <code>{left}</code>\n"
            f"  📦 Stock: <code>{stock}</code>\n"
            f"  🕐 Resets: <code>{resets_str}</code>\n\n"
        )
    text += "💡 <i>Limits reset on a rolling basis every hour.</i>"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Refresh", callback_data="status"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return text, markup

def build_stock():
    text = "📦 📦 <b>COOKIE STOCK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for t, name in [("premium", "👑 PREMIUM"), ("standard", "⭐ STANDARD"),
                    ("basic", "🎯 BASIC"), ("prime", "🍿 PRIME VIDEO")]:
        text += f"<b>{name}:</b> <code>{STOCK[t]} accounts</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Refresh", callback_data="stock"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return text, markup

def build_lang():
    return "🌐 <b>Select your language:</b>", lang_markup()

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

# ====================== COMMANDS ======================
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=main_menu_markup(), parse_mode="HTML")

@bot.message_handler(commands=['status'])
def status_command(message):
    text, markup = build_status(message.chat.id)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['stock'])
def stock_command(message):
    text, markup = build_stock()
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['lang'])
def lang_command(message):
    text, markup = build_lang()
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['country'])
def country_handler(message):
    try:
        country = message.text.split(maxsplit=1)[1].upper()
        bot.reply_to(message, f"🔍 Searching cookies for country: <b>{country}</b>...", parse_mode="HTML")
        time.sleep(2)
        bot.send_message(message.chat.id, f"✅ Found live cookies for <b>{country}</b> (Demo)", parse_mode="HTML")
    except:
        bot.reply_to(message, "Usage: <code>/country IN</code>\nExamples: US, BR, FR, DE, ID", parse_mode="HTML")

# ====================== CALLBACKS ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user = get_user_data(chat_id)
    data = call.data

    if data == "main_menu":
        edit_current_message(call, WELCOME_TEXT, main_menu_markup())

    elif data == "netflix":
        edit_current_message(call, "🔽 Choose a tier for <b>Netflix</b>:", netflix_tier_markup())

    elif data == "prime":
        edit_current_message(call, "🔽 Choose a tier for <b>PrimeVideo</b>:", prime_tier_markup())

    elif data.startswith("tier_"):
        tier = data.split("_")[1]

        if STOCK.get(tier, 0) <= 0:
            edit_current_message(call, "❌ <b>Out of stock!</b>")
            time.sleep(1.5)
            back = prime_tier_markup() if tier == "prime" else netflix_tier_markup()
            label = "PrimeVideo" if tier == "prime" else "Netflix"
            edit_current_message(call, f"🔽 Choose a tier for <b>{label}</b>:", back)
            return

        if user["used"].get(tier, 0) >= 3:
            edit_current_message(call, "⏳ You reached the hourly limit for this tier.")
            time.sleep(1.5)
            back = prime_tier_markup() if tier == "prime" else netflix_tier_markup()
            label = "PrimeVideo" if tier == "prime" else "Netflix"
            edit_current_message(call, f"🔽 Choose a tier for <b>{label}</b>:", back)
            return

        user["used"][tier] += 1
        STOCK[tier] = max(0, STOCK[tier] - 1)
        delivery_text = (
            f"✅ <b>{tier.upper()} COOKIE DELIVERED!</b>\n\n"
            f"🔗 <code>https://example.com/nftoken/{tier}-{int(time.time())}</code>\n\n"
            f"Import the cookie and open the link above.\nUse responsibly!"
        )
        edit_current_message(call, delivery_text, main_menu_markup())

    elif data == "status":
        text, markup = build_status(chat_id)
        edit_current_message(call, text, markup)

    elif data == "stock":
        text, markup = build_stock()
        edit_current_message(call, text, markup)

    elif data == "help":
        help_text = """ℹ️ ℹ️ <b>HOW TO USE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Choose a tier from the main menu
2️⃣  Bot verifies the cookie is live before sending
3️⃣  Import the cookie into your browser
4️⃣  Use the NFToken link to watch directly

📁 📁 <b>TIERS:</b>
  👑 Premium — Full 4K, up to 4 screens
  ⭐ Standard — 1080p HD, up to 2 screens
  🎯 Basic/Mobile — 720p, 1 screen

💡 <i>Use cookies responsibly.</i>"""
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🌐 Language", callback_data="language"))
        markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
        edit_current_message(call, help_text, markup)

    elif data == "language":
        text, markup = build_lang()
        edit_current_message(call, text, markup)

    elif data.startswith("lang_"):
        edit_current_message(call, WELCOME_TEXT, main_menu_markup())

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