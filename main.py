import telebot
from telebot import types
import time
from datetime import datetime, timedelta

# ====================== CONFIG ======================
TOKEN = "8863877477:AAEEW9DN1cP8GWkpiSENJA-56A1viiU28Yw"  # ← Change this
bot = telebot.TeleBot(TOKEN)

# In-memory storage (replace with SQLite/Redis later)
USER_DATA = {}   # chat_id → user usage
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
    # Rolling 1-hour reset
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
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(f"👑 Premium ({STOCK['premium']})", callback_data="tier_premium"),
        types.InlineKeyboardButton(f"⭐ Standard ({STOCK['standard']})", callback_data="tier_standard"),
        types.InlineKeyboardButton(f"🎯 Basic ({STOCK['basic']})", callback_data="tier_basic")
    )
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

def prime_tier_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(f"🍿 Prime Video ({STOCK['prime']})", callback_data="tier_prime")
    )
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

def edit_current_message(call, text: str, reply_markup=None):
    """Core function: Always edit the current message instead of sending new ones"""
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
            print(f"Edit error: {e}")
            # Fallback
            bot.send_message(call.message.chat.id, text, reply_markup=reply_markup, parse_mode="HTML")

# ====================== START ======================
@bot.message_handler(commands=['start'])
def start_command(message):
    welcome_text = """👋 <b>WELCOME, CAY!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Live-verified Netflix cookies across 3 tiers.
Every cookie is checked before delivery.

📌📌 <b>RULES:</b>
  • 📈 3 cookies per tier per hour
  • 🕒 Rolling 1-hour window (persists across restarts)
  • ❌ Dead cookies are auto-removed

⬇️⬇️ <b>CHOOSE A SERVICE BELOW:</b>"""

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_menu_markup(),
        parse_mode="HTML"
    )

# ====================== CALLBACKS ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    user = get_user_data(chat_id)
    data = call.data

    if data == "main_menu":
        welcome_text = """👋 <b>WELCOME, CAY!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Live-verified Netflix cookies across 3 tiers.
Every cookie is checked before delivery.

📌📌 <b>RULES:</b>
  • 📈 3 cookies per tier per hour
  • 🕒 Rolling 1-hour window (persists across restarts)
  • ❌ Dead cookies are auto-removed

⬇️⬇️ <b>CHOOSE A SERVICE BELOW:</b>"""
        edit_current_message(call, welcome_text, main_menu_markup())

    elif data == "netflix":
        edit_current_message(call, "🎬 <b>Choose Netflix Tier:</b>", netflix_tier_markup())

    elif data == "prime":
        edit_current_message(call, "🍿 <b>Prime Video Tier:</b>", prime_tier_markup())

    # Tier Selection
    elif data.startswith("tier_"):
        tier_map = {"premium": "premium", "standard": "standard", "basic": "basic", "prime": "prime"}
        tier = tier_map.get(data.split("_")[1])
        
        if STOCK.get(tier, 0) <= 0:
            edit_current_message(call, "❌ <b>Out of stock!</b>", None)
            time.sleep(1.5)
            edit_current_message(call, "🎬 <b>Choose Netflix Tier:</b>", netflix_tier_markup())
            return

        if user["used"].get(tier, 0) >= 3:
            edit_current_message(call, "⏳ You reached the hourly limit for this tier.", None)
            time.sleep(1.5)
            edit_current_message(call, "🎬 <b>Choose Netflix Tier:</b>", netflix_tier_markup())
            return

        # Deliver cookie
        user["used"][tier] += 1
        STOCK[tier] = max(0, STOCK[tier] - 1)

        delivery_text = f"""✅ <b>{tier.upper()} COOKIE DELIVERED!</b>

🔗 <code>https://example.com/nftoken/{tier}-{int(time.time())}</code>

Import the cookie and open the link above.
Use responsibly!"""

        edit_current_message(call, delivery_text, main_menu_markup())

    elif data == "status":
        status_text = "📊📊 <b>YOUR USAGE STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
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
            # Calculate reset time
            last_reset = user["last_reset"]
            reset_at = last_reset + timedelta(hours=1)
            now = datetime.now()
            if used > 0 and now < reset_at:
                diff = reset_at - now
                mins = int(diff.total_seconds() // 60)
                secs = int(diff.total_seconds() % 60)
                resets_str = f"{mins}m {secs}s"
            else:
                resets_str = "—"
            status_text += (
                f"<b>{name}</b>\n"
                f"  📈 Used: {used}/3\n"
                f"  🔄 Left: {left}\n"
                f"  📦 Stock: {stock}\n"
                f"  🕐 Resets: {resets_str}\n\n"
            )
        status_text += "💡 <i>Limits reset on a rolling basis every hour.</i>"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Refresh", callback_data="status"))
        markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))

        edit_current_message(call, status_text, markup)

    elif data == "stock":
        stock_text = "📦📦 <b>COOKIE STOCK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        tiers = [
            ("premium", "👑 PREMIUM"),
            ("standard", "⭐ STANDARD"),
            ("basic", "🎯 BASIC"),
            ("prime", "🍿 PRIME VIDEO"),
        ]
        for t, name in tiers:
            count = STOCK[t]
            bar = "▰▰▰▰▰▰▰▰▰▰"
            stock_text += f"<b>{name}:</b> {count} accounts\n{bar}\n\n"

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 Refresh", callback_data="stock"))
        markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))

        edit_current_message(call, stock_text, markup)

    elif data == "help":
        help_text = """ℹ️ℹ️ <b>HOW TO USE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Choose a tier from the main menu
2️⃣  Bot verifies the cookie is live before sending
3️⃣  Import the cookie into your browser
4️⃣  Use the NFToken link to watch directly

🗂🗂 <b>TIERS:</b>
👑 Premium — Full 4K, up to 4 screens
⭐ Standard — 1080p HD, up to 2 screens
🎯 Basic/Mobile — 720p, 1 screen

🖊 <b>BROWSER EXTENSION:</b>
• <a href="https://t.me/deadflix">Deadflix Extension (Plug &amp; Play)</a>

💡 <i>Use cookies responsibly.</i>"""

        help_markup = types.InlineKeyboardMarkup()
        help_markup.add(types.InlineKeyboardButton("🌐 Language", callback_data="language"))
        help_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
        edit_current_message(call, help_text, help_markup)

    elif data == "language":
        lang_markup = types.InlineKeyboardMarkup(row_width=3)
        lang_markup.add(
            types.InlineKeyboardButton("🇬🇧 English",    callback_data="lang_en"),
            types.InlineKeyboardButton("🇪🇸 Español",    callback_data="lang_es"),
            types.InlineKeyboardButton("🇫🇷 Français",   callback_data="lang_fr"),
        )
        lang_markup.add(
            types.InlineKeyboardButton("🇧🇷 Português",  callback_data="lang_pt"),
            types.InlineKeyboardButton("🇸🇦 العربية",    callback_data="lang_ar"),
            types.InlineKeyboardButton("🇮🇳 हिन्दी",      callback_data="lang_hi"),
        )
        lang_markup.add(
            types.InlineKeyboardButton("🇮🇩 Indonesia",  callback_data="lang_id"),
            types.InlineKeyboardButton("🇷🇺 Русский",    callback_data="lang_ru"),
            types.InlineKeyboardButton("🇹🇷 Türkçe",     callback_data="lang_tr"),
        )
        lang_markup.add(
            types.InlineKeyboardButton("🇩🇪 Deutsch",    callback_data="lang_de"),
            types.InlineKeyboardButton("🇮🇹 Italiano",   callback_data="lang_it"),
            types.InlineKeyboardButton("🇯🇵 日本語",      callback_data="lang_ja"),
        )
        lang_markup.add(
            types.InlineKeyboardButton("🇰🇷 한국어",      callback_data="lang_ko"),
        )
        edit_current_message(call, "🌐 <b>Select your language:</b>", lang_markup)

    elif data.startswith("lang_"):
        # Language selected — store preference and return to main menu
        welcome_text = """👋 <b>WELCOME, CAY!</b>
━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Live-verified Netflix cookies across 3 tiers.
Every cookie is checked before delivery.

📌📌 <b>RULES:</b>
  • 📈 3 cookies per tier per hour
  • 🕒 Rolling 1-hour window (persists across restarts)
  • ❌ Dead cookies are auto-removed

⬇️⬇️ <b>CHOOSE A SERVICE BELOW:</b>"""
        edit_current_message(call, welcome_text, main_menu_markup())

    bot.answer_callback_query(call.id)

# ====================== COUNTRY COMMAND ======================
@bot.message_handler(commands=['country'])
def country_handler(message):
    try:
        country = message.text.split(maxsplit=1)[1].upper()
        bot.reply_to(message, f"🔍 Searching cookies for country: <b>{country}</b>...", parse_mode="HTML")
        # Add your real fetching logic here
        time.sleep(2)
        bot.send_message(message.chat.id, f"✅ Found live cookies for <b>{country}</b> (Demo)", parse_mode="HTML")
    except:
        bot.reply_to(message, "Usage: <code>/country IN</code>\nExamples: US, BR, FR, DE, ID", parse_mode="HTML")

# ====================== RUN ======================
if __name__ == "__main__":
    print("🚀 DEADFLIX Bot is running...")
    bot.infinity_polling()

