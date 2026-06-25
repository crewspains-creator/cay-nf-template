# ====================== LANGUAGES ======================
# All UI strings live here. Add a new language by copying
# any existing block, changing the key, and translating.
# Keys must match exactly — the bot falls back to "en" if a key is missing.

LANGUAGES = {

    "en": {
        "name": "🇬🇧 English",
        "welcome": (
            "👋 <b>WELCOME, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Live-verified Netflix cookies across 3 tiers.\n"
            "Every cookie is checked before delivery.\n\n"
            "📌 📌 <b>RULES:</b>\n"
            "  • 📈 3 cookies per tier per hour\n"
            "  • ⏱️ Rolling 1-hour window (persists across restarts)\n"
            "  • ❌ Dead cookies are auto-removed\n\n"
            "🔽 🔽 <b>CHOOSE A SERVICE BELOW:</b>"
        ),
        "choose_netflix":   "🔽 Choose a tier for <b>Netflix</b>:",
        "choose_prime":     "🔽 Choose a tier for <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Out of stock!</b>",
        "hourly_limit":     "⏳ You reached the hourly limit for this tier.",
        "cookie_delivered": "✅ <b>{tier} COOKIE DELIVERED!</b>\n\n🔗 <code>{url}</code>\n\nImport the cookie and open the link above.\nUse responsibly!",
        "status_title":     "📊📊 <b>YOUR USAGE STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Used: <code>{used}/3</code>\n  🔄 Left: <code>{left}</code>\n  📦 Stock: <code>{stock}</code>\n  🕐 Resets: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Limits reset on a rolling basis every hour.</i>",
        "stock_title":      "📦 📦 <b>COOKIE STOCK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} accounts</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>HOW TO USE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Choose a tier from the main menu\n"
            "2️⃣  Bot verifies the cookie is live before sending\n"
            "3️⃣  Import the cookie into your browser\n"
            "4️⃣  Use the NFToken link to watch directly\n\n"
            "📁 📁 <b>TIERS:</b>\n"
            "  👑 Premium — Full 4K, up to 4 screens\n"
            "  ⭐ Standard — 1080p HD, up to 2 screens\n"
            "  🎯 Basic/Mobile — 720p, 1 screen\n\n"
            "💡 <i>Use cookies responsibly.</i>"
        ),
        "select_language":  "🌐 <b>Select your language:</b>",
        "resets_soon":      "{m}m {s}s",
        "resets_none":      "—",
        # Buttons
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Status",
        "btn_stock":        "📦 Stock",
        "btn_help":         "ℹ️ Help",
        "btn_language":     "🌐 Language",
        "btn_main_menu":    "🏠 Main Menu",
        "btn_refresh":      "🔄 Refresh",
        "btn_by_country":   "🌍 By Country",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Basic ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Searching cookies for country: <b>{country}</b>...",
        "country_found":    "✅ Found live cookies for <b>{country}</b> (Demo)",
        "country_usage":    "Usage: <code>/country IN</code>\nExamples: US, BR, FR, DE, ID",
        # Tier display names (used in status)
        "tier_premium":     "👑 PREMIUM TIER",
        "tier_standard":    "⭐ STANDARD TIER",
        "tier_basic":       "🎯 BASIC TIER",
        "tier_prime":       "🍿 PRIME VIDEO TIER",
        # Stock display names
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BASIC",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "es": {
        "name": "🇪🇸 Español",
        "welcome": (
            "👋 <b>¡BIENVENIDO, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Cookies de Netflix verificadas en vivo en 3 niveles.\n"
            "Cada cookie se verifica antes de la entrega.\n\n"
            "📌 📌 <b>REGLAS:</b>\n"
            "  • 📈 3 cookies por nivel por hora\n"
            "  • ⏱️ Ventana de 1 hora continua\n"
            "  • ❌ Las cookies muertas se eliminan automáticamente\n\n"
            "🔽 🔽 <b>ELIGE UN SERVICIO:</b>"
        ),
        "choose_netflix":   "🔽 Elige un nivel para <b>Netflix</b>:",
        "choose_prime":     "🔽 Elige un nivel para <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>¡Sin stock!</b>",
        "hourly_limit":     "⏳ Alcanzaste el límite por hora para este nivel.",
        "cookie_delivered": "✅ <b>¡COOKIE {tier} ENTREGADA!</b>\n\n🔗 <code>{url}</code>\n\nImporta la cookie y abre el enlace.\n¡Úsala responsablemente!",
        "status_title":     "📊📊 <b>TU ESTADO DE USO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Usado: <code>{used}/3</code>\n  🔄 Restante: <code>{left}</code>\n  📦 Stock: <code>{stock}</code>\n  🕐 Reinicia: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Los límites se reinician cada hora de forma continua.</i>",
        "stock_title":      "📦 📦 <b>STOCK DE COOKIES</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} cuentas</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>CÓMO USAR</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Elige un nivel desde el menú principal\n"
            "2️⃣  El bot verifica que la cookie esté activa\n"
            "3️⃣  Importa la cookie en tu navegador\n"
            "4️⃣  Usa el enlace NFToken para ver directamente\n\n"
            "📁 📁 <b>NIVELES:</b>\n"
            "  👑 Premium — 4K completo, hasta 4 pantallas\n"
            "  ⭐ Estándar — 1080p HD, hasta 2 pantallas\n"
            "  🎯 Básico/Móvil — 720p, 1 pantalla\n\n"
            "💡 <i>Usa las cookies responsablemente.</i>"
        ),
        "select_language":  "🌐 <b>Selecciona tu idioma:</b>",
        "resets_soon":      "{m}m {s}s",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Estado",
        "btn_stock":        "📦 Stock",
        "btn_help":         "ℹ️ Ayuda",
        "btn_language":     "🌐 Idioma",
        "btn_main_menu":    "🏠 Menú Principal",
        "btn_refresh":      "🔄 Actualizar",
        "btn_by_country":   "🌍 Por País",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Estándar ({n})",
        "btn_basic":        "🎯 Básico ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Buscando cookies para: <b>{country}</b>...",
        "country_found":    "✅ Cookies encontradas para <b>{country}</b> (Demo)",
        "country_usage":    "Uso: <code>/country IN</code>\nEjemplos: US, BR, FR, DE, ID",
        "tier_premium":     "👑 NIVEL PREMIUM",
        "tier_standard":    "⭐ NIVEL ESTÁNDAR",
        "tier_basic":       "🎯 NIVEL BÁSICO",
        "tier_prime":       "🍿 NIVEL PRIME VIDEO",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ ESTÁNDAR",
        "stock_basic":      "🎯 BÁSICO",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "fr": {
        "name": "🇫🇷 Français",
        "welcome": (
            "👋 <b>BIENVENUE, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Cookies Netflix vérifiés en direct sur 3 niveaux.\n"
            "Chaque cookie est vérifié avant livraison.\n\n"
            "📌 📌 <b>RÈGLES:</b>\n"
            "  • 📈 3 cookies par niveau par heure\n"
            "  • ⏱️ Fenêtre d'1 heure glissante\n"
            "  • ❌ Les cookies morts sont supprimés automatiquement\n\n"
            "🔽 🔽 <b>CHOISISSEZ UN SERVICE:</b>"
        ),
        "choose_netflix":   "🔽 Choisissez un niveau pour <b>Netflix</b>:",
        "choose_prime":     "🔽 Choisissez un niveau pour <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Rupture de stock!</b>",
        "hourly_limit":     "⏳ Vous avez atteint la limite horaire pour ce niveau.",
        "cookie_delivered": "✅ <b>COOKIE {tier} LIVRÉ!</b>\n\n🔗 <code>{url}</code>\n\nImportez le cookie et ouvrez le lien.\nUtilisez-le de manière responsable!",
        "status_title":     "📊📊 <b>VOTRE STATUT D'UTILISATION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Utilisé: <code>{used}/3</code>\n  🔄 Restant: <code>{left}</code>\n  📦 Stock: <code>{stock}</code>\n  🕐 Réinitialise: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Les limites se réinitialisent toutes les heures de manière glissante.</i>",
        "stock_title":      "📦 📦 <b>STOCK DE COOKIES</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} comptes</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>COMMENT UTILISER</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Choisissez un niveau dans le menu principal\n"
            "2️⃣  Le bot vérifie que le cookie est actif\n"
            "3️⃣  Importez le cookie dans votre navigateur\n"
            "4️⃣  Utilisez le lien NFToken pour regarder\n\n"
            "📁 📁 <b>NIVEAUX:</b>\n"
            "  👑 Premium — 4K complet, jusqu'à 4 écrans\n"
            "  ⭐ Standard — 1080p HD, jusqu'à 2 écrans\n"
            "  🎯 Basique/Mobile — 720p, 1 écran\n\n"
            "💡 <i>Utilisez les cookies de manière responsable.</i>"
        ),
        "select_language":  "🌐 <b>Sélectionnez votre langue:</b>",
        "resets_soon":      "{m}m {s}s",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Statut",
        "btn_stock":        "📦 Stock",
        "btn_help":         "ℹ️ Aide",
        "btn_language":     "🌐 Langue",
        "btn_main_menu":    "🏠 Menu Principal",
        "btn_refresh":      "🔄 Actualiser",
        "btn_by_country":   "🌍 Par Pays",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Basique ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Recherche de cookies pour: <b>{country}</b>...",
        "country_found":    "✅ Cookies trouvés pour <b>{country}</b> (Démo)",
        "country_usage":    "Usage: <code>/country IN</code>\nExemples: US, BR, FR, DE, ID",
        "tier_premium":     "👑 NIVEAU PREMIUM",
        "tier_standard":    "⭐ NIVEAU STANDARD",
        "tier_basic":       "🎯 NIVEAU BASIQUE",
        "tier_prime":       "🍿 NIVEAU PRIME VIDEO",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BASIQUE",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "pt": {
        "name": "🇧🇷 Português",
        "welcome": (
            "👋 <b>BEM-VINDO, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Cookies Netflix verificados ao vivo em 3 níveis.\n"
            "Cada cookie é verificado antes da entrega.\n\n"
            "📌 📌 <b>REGRAS:</b>\n"
            "  • 📈 3 cookies por nível por hora\n"
            "  • ⏱️ Janela de 1 hora contínua\n"
            "  • ❌ Cookies mortos são removidos automaticamente\n\n"
            "🔽 🔽 <b>ESCOLHA UM SERVIÇO:</b>"
        ),
        "choose_netflix":   "🔽 Escolha um nível para <b>Netflix</b>:",
        "choose_prime":     "🔽 Escolha um nível para <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Sem estoque!</b>",
        "hourly_limit":     "⏳ Você atingiu o limite por hora para este nível.",
        "cookie_delivered": "✅ <b>COOKIE {tier} ENTREGUE!</b>\n\n🔗 <code>{url}</code>\n\nImporte o cookie e abra o link.\nUse com responsabilidade!",
        "status_title":     "📊📊 <b>SEU STATUS DE USO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Usado: <code>{used}/3</code>\n  🔄 Restante: <code>{left}</code>\n  📦 Estoque: <code>{stock}</code>\n  🕐 Reinicia: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Os limites são redefinidos a cada hora de forma contínua.</i>",
        "stock_title":      "📦 📦 <b>ESTOQUE DE COOKIES</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} contas</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>COMO USAR</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Escolha um nível no menu principal\n"
            "2️⃣  O bot verifica se o cookie está ativo\n"
            "3️⃣  Importe o cookie no seu navegador\n"
            "4️⃣  Use o link NFToken para assistir\n\n"
            "📁 📁 <b>NÍVEIS:</b>\n"
            "  👑 Premium — 4K completo, até 4 telas\n"
            "  ⭐ Standard — 1080p HD, até 2 telas\n"
            "  🎯 Básico/Mobile — 720p, 1 tela\n\n"
            "💡 <i>Use os cookies com responsabilidade.</i>"
        ),
        "select_language":  "🌐 <b>Selecione seu idioma:</b>",
        "resets_soon":      "{m}m {s}s",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Status",
        "btn_stock":        "📦 Estoque",
        "btn_help":         "ℹ️ Ajuda",
        "btn_language":     "🌐 Idioma",
        "btn_main_menu":    "🏠 Menu Principal",
        "btn_refresh":      "🔄 Atualizar",
        "btn_by_country":   "🌍 Por País",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Básico ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Buscando cookies para: <b>{country}</b>...",
        "country_found":    "✅ Cookies encontrados para <b>{country}</b> (Demo)",
        "country_usage":    "Uso: <code>/country IN</code>\nExemplos: US, BR, FR, DE, ID",
        "tier_premium":     "👑 NÍVEL PREMIUM",
        "tier_standard":    "⭐ NÍVEL STANDARD",
        "tier_basic":       "🎯 NÍVEL BÁSICO",
        "tier_prime":       "🍿 NÍVEL PRIME VIDEO",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BÁSICO",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "ar": {
        "name": "🇸🇦 العربية",
        "welcome": (
            "👋 <b>مرحباً، CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ كوكيز Netflix مُتحقَّق منها مباشرةً عبر 3 مستويات.\n"
            "يتم فحص كل كوكي قبل التسليم.\n\n"
            "📌 📌 <b>القواعد:</b>\n"
            "  • 📈 3 كوكيز لكل مستوى في الساعة\n"
            "  • ⏱️ نافذة ساعة واحدة متجددة\n"
            "  • ❌ تتم إزالة الكوكيز الميتة تلقائياً\n\n"
            "🔽 🔽 <b>اختر خدمة:</b>"
        ),
        "choose_netflix":   "🔽 اختر مستوى لـ <b>Netflix</b>:",
        "choose_prime":     "🔽 اختر مستوى لـ <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>نفد المخزون!</b>",
        "hourly_limit":     "⏳ لقد وصلت إلى الحد الساعي لهذا المستوى.",
        "cookie_delivered": "✅ <b>تم تسليم كوكي {tier}!</b>\n\n🔗 <code>{url}</code>\n\nاستورد الكوكي وافتح الرابط.\nاستخدمه بمسؤولية!",
        "status_title":     "📊📊 <b>حالة استخدامك</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 المُستخدَم: <code>{used}/3</code>\n  🔄 المتبقي: <code>{left}</code>\n  📦 المخزون: <code>{stock}</code>\n  🕐 إعادة ضبط: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>تُعاد الحدود كل ساعة بشكل متجدد.</i>",
        "stock_title":      "📦 📦 <b>مخزون الكوكيز</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} حسابات</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>كيفية الاستخدام</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  اختر مستوى من القائمة الرئيسية\n"
            "2️⃣  يتحقق البوت من أن الكوكي نشط\n"
            "3️⃣  استورد الكوكي في متصفحك\n"
            "4️⃣  استخدم رابط NFToken للمشاهدة\n\n"
            "📁 📁 <b>المستويات:</b>\n"
            "  👑 بريميوم — 4K كامل، حتى 4 شاشات\n"
            "  ⭐ ستاندرد — 1080p HD، حتى شاشتين\n"
            "  🎯 أساسي/موبايل — 720p، شاشة واحدة\n\n"
            "💡 <i>استخدم الكوكيز بمسؤولية.</i>"
        ),
        "select_language":  "🌐 <b>اختر لغتك:</b>",
        "resets_soon":      "{m}د {s}ث",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 الحالة",
        "btn_stock":        "📦 المخزون",
        "btn_help":         "ℹ️ مساعدة",
        "btn_language":     "🌐 اللغة",
        "btn_main_menu":    "🏠 القائمة الرئيسية",
        "btn_refresh":      "🔄 تحديث",
        "btn_by_country":   "🌍 حسب الدولة",
        "btn_premium":      "👑 بريميوم ({n})",
        "btn_standard":     "⭐ ستاندرد ({n})",
        "btn_basic":        "🎯 أساسي ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 البحث عن كوكيز لـ: <b>{country}</b>...",
        "country_found":    "✅ تم العثور على كوكيز لـ <b>{country}</b> (تجريبي)",
        "country_usage":    "الاستخدام: <code>/country IN</code>\nأمثلة: US, BR, FR, DE, ID",
        "tier_premium":     "👑 مستوى بريميوم",
        "tier_standard":    "⭐ مستوى ستاندرد",
        "tier_basic":       "🎯 المستوى الأساسي",
        "tier_prime":       "🍿 مستوى Prime Video",
        "stock_premium":    "👑 بريميوم",
        "stock_standard":   "⭐ ستاندرد",
        "stock_basic":      "🎯 أساسي",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "hi": {
        "name": "🇮🇳 हिन्दी",
        "welcome": (
            "👋 <b>स्वागत है, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ 3 टियर में लाइव-वेरिफाइड Netflix कुकीज़।\n"
            "हर कुकी डिलीवरी से पहले चेक की जाती है।\n\n"
            "📌 📌 <b>नियम:</b>\n"
            "  • 📈 प्रति टियर प्रति घंटे 3 कुकीज़\n"
            "  • ⏱️ रोलिंग 1 घंटे की विंडो\n"
            "  • ❌ मृत कुकीज़ स्वचालित रूप से हटा दी जाती हैं\n\n"
            "🔽 🔽 <b>नीचे एक सेवा चुनें:</b>"
        ),
        "choose_netflix":   "🔽 <b>Netflix</b> के लिए एक टियर चुनें:",
        "choose_prime":     "🔽 <b>PrimeVideo</b> के लिए एक टियर चुनें:",
        "out_of_stock":     "❌ <b>स्टॉक खत्म!</b>",
        "hourly_limit":     "⏳ आप इस टियर की घंटे की सीमा तक पहुँच गए।",
        "cookie_delivered": "✅ <b>{tier} कुकी डिलीवर हुई!</b>\n\n🔗 <code>{url}</code>\n\nकुकी इम्पोर्ट करें और लिंक खोलें।\nजिम्मेदारी से उपयोग करें!",
        "status_title":     "📊📊 <b>आपकी उपयोग स्थिति</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 उपयोग: <code>{used}/3</code>\n  🔄 शेष: <code>{left}</code>\n  📦 स्टॉक: <code>{stock}</code>\n  🕐 रीसेट: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>सीमाएँ हर घंटे रोलिंग आधार पर रीसेट होती हैं।</i>",
        "stock_title":      "📦 📦 <b>कुकी स्टॉक</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} अकाउंट</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>उपयोग कैसे करें</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  मुख्य मेनू से एक टियर चुनें\n"
            "2️⃣  बॉट कुकी को लाइव वेरिफाई करता है\n"
            "3️⃣  कुकी को अपने ब्राउज़र में इम्पोर्ट करें\n"
            "4️⃣  सीधे देखने के लिए NFToken लिंक का उपयोग करें\n\n"
            "📁 📁 <b>टियर:</b>\n"
            "  👑 प्रीमियम — पूर्ण 4K, 4 स्क्रीन तक\n"
            "  ⭐ स्टैंडर्ड — 1080p HD, 2 स्क्रीन तक\n"
            "  🎯 बेसिक/मोबाइल — 720p, 1 स्क्रीन\n\n"
            "💡 <i>कुकीज़ का जिम्मेदारी से उपयोग करें।</i>"
        ),
        "select_language":  "🌐 <b>अपनी भाषा चुनें:</b>",
        "resets_soon":      "{m}मि {s}से",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 स्थिति",
        "btn_stock":        "📦 स्टॉक",
        "btn_help":         "ℹ️ सहायता",
        "btn_language":     "🌐 भाषा",
        "btn_main_menu":    "🏠 मुख्य मेनू",
        "btn_refresh":      "🔄 रिफ्रेश",
        "btn_by_country":   "🌍 देश अनुसार",
        "btn_premium":      "👑 प्रीमियम ({n})",
        "btn_standard":     "⭐ स्टैंडर्ड ({n})",
        "btn_basic":        "🎯 बेसिक ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 <b>{country}</b> के लिए कुकीज़ खोज रहे हैं...",
        "country_found":    "✅ <b>{country}</b> के लिए लाइव कुकीज़ मिलीं (डेमो)",
        "country_usage":    "उपयोग: <code>/country IN</code>\nउदाहरण: US, BR, FR, DE, ID",
        "tier_premium":     "👑 प्रीमियम टियर",
        "tier_standard":    "⭐ स्टैंडर्ड टियर",
        "tier_basic":       "🎯 बेसिक टियर",
        "tier_prime":       "🍿 PRIME VIDEO टियर",
        "stock_premium":    "👑 प्रीमियम",
        "stock_standard":   "⭐ स्टैंडर्ड",
        "stock_basic":      "🎯 बेसिक",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "id": {
        "name": "🇮🇩 Indonesia",
        "welcome": (
            "👋 <b>SELAMAT DATANG, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Cookie Netflix terverifikasi langsung di 3 tingkatan.\n"
            "Setiap cookie dicek sebelum dikirim.\n\n"
            "📌 📌 <b>ATURAN:</b>\n"
            "  • 📈 3 cookie per tingkat per jam\n"
            "  • ⏱️ Jendela 1 jam bergulir\n"
            "  • ❌ Cookie mati dihapus otomatis\n\n"
            "🔽 🔽 <b>PILIH LAYANAN:</b>"
        ),
        "choose_netflix":   "🔽 Pilih tingkatan untuk <b>Netflix</b>:",
        "choose_prime":     "🔽 Pilih tingkatan untuk <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Stok habis!</b>",
        "hourly_limit":     "⏳ Anda mencapai batas per jam untuk tingkatan ini.",
        "cookie_delivered": "✅ <b>COOKIE {tier} TERKIRIM!</b>\n\n🔗 <code>{url}</code>\n\nImpor cookie dan buka tautan.\nGunakan dengan bijak!",
        "status_title":     "📊📊 <b>STATUS PENGGUNAAN ANDA</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Dipakai: <code>{used}/3</code>\n  🔄 Sisa: <code>{left}</code>\n  📦 Stok: <code>{stock}</code>\n  🕐 Reset: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Batas diatur ulang setiap jam secara bergulir.</i>",
        "stock_title":      "📦 📦 <b>STOK COOKIE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} akun</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>CARA PENGGUNAAN</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Pilih tingkatan dari menu utama\n"
            "2️⃣  Bot memverifikasi cookie masih aktif\n"
            "3️⃣  Impor cookie ke browser Anda\n"
            "4️⃣  Gunakan tautan NFToken untuk menonton\n\n"
            "📁 📁 <b>TINGKATAN:</b>\n"
            "  👑 Premium — 4K penuh, hingga 4 layar\n"
            "  ⭐ Standard — 1080p HD, hingga 2 layar\n"
            "  🎯 Basic/Mobile — 720p, 1 layar\n\n"
            "💡 <i>Gunakan cookie dengan bijak.</i>"
        ),
        "select_language":  "🌐 <b>Pilih bahasa Anda:</b>",
        "resets_soon":      "{m}m {s}d",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Status",
        "btn_stock":        "📦 Stok",
        "btn_help":         "ℹ️ Bantuan",
        "btn_language":     "🌐 Bahasa",
        "btn_main_menu":    "🏠 Menu Utama",
        "btn_refresh":      "🔄 Segarkan",
        "btn_by_country":   "🌍 Per Negara",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Basic ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Mencari cookie untuk: <b>{country}</b>...",
        "country_found":    "✅ Cookie ditemukan untuk <b>{country}</b> (Demo)",
        "country_usage":    "Penggunaan: <code>/country IN</code>\nContoh: US, BR, FR, DE, ID",
        "tier_premium":     "👑 TINGKAT PREMIUM",
        "tier_standard":    "⭐ TINGKAT STANDARD",
        "tier_basic":       "🎯 TINGKAT BASIC",
        "tier_prime":       "🍿 TINGKAT PRIME VIDEO",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BASIC",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "ru": {
        "name": "🇷🇺 Русский",
        "welcome": (
            "👋 <b>ДОБРО ПОЖАЛОВАТЬ, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Живые куки Netflix в 3 уровнях.\n"
            "Каждый куки проверяется перед отправкой.\n\n"
            "📌 📌 <b>ПРАВИЛА:</b>\n"
            "  • 📈 3 куки на уровень в час\n"
            "  • ⏱️ Скользящее окно 1 час\n"
            "  • ❌ Мёртвые куки удаляются автоматически\n\n"
            "🔽 🔽 <b>ВЫБЕРИТЕ СЕРВИС:</b>"
        ),
        "choose_netflix":   "🔽 Выберите уровень для <b>Netflix</b>:",
        "choose_prime":     "🔽 Выберите уровень для <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Нет в наличии!</b>",
        "hourly_limit":     "⏳ Вы достигли часового лимита для этого уровня.",
        "cookie_delivered": "✅ <b>КУКИ {tier} ДОСТАВЛЕН!</b>\n\n🔗 <code>{url}</code>\n\nИмпортируйте куки и откройте ссылку.\nИспользуйте ответственно!",
        "status_title":     "📊📊 <b>СТАТУС ИСПОЛЬЗОВАНИЯ</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Использовано: <code>{used}/3</code>\n  🔄 Осталось: <code>{left}</code>\n  📦 Запас: <code>{stock}</code>\n  🕐 Сброс: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Лимиты сбрасываются каждый час по скользящему графику.</i>",
        "stock_title":      "📦 📦 <b>ЗАПАС КУКИ</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} аккаунтов</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>КАК ПОЛЬЗОВАТЬСЯ</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Выберите уровень в главном меню\n"
            "2️⃣  Бот проверяет активность куки\n"
            "3️⃣  Импортируйте куки в браузер\n"
            "4️⃣  Используйте NFToken ссылку для просмотра\n\n"
            "📁 📁 <b>УРОВНИ:</b>\n"
            "  👑 Премиум — 4K, до 4 экранов\n"
            "  ⭐ Стандарт — 1080p HD, до 2 экранов\n"
            "  🎯 Базовый/Мобильный — 720p, 1 экран\n\n"
            "💡 <i>Используйте куки ответственно.</i>"
        ),
        "select_language":  "🌐 <b>Выберите язык:</b>",
        "resets_soon":      "{m}м {s}с",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Статус",
        "btn_stock":        "📦 Запас",
        "btn_help":         "ℹ️ Помощь",
        "btn_language":     "🌐 Язык",
        "btn_main_menu":    "🏠 Главное меню",
        "btn_refresh":      "🔄 Обновить",
        "btn_by_country":   "🌍 По стране",
        "btn_premium":      "👑 Премиум ({n})",
        "btn_standard":     "⭐ Стандарт ({n})",
        "btn_basic":        "🎯 Базовый ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Ищу куки для: <b>{country}</b>...",
        "country_found":    "✅ Найдены куки для <b>{country}</b> (Демо)",
        "country_usage":    "Использование: <code>/country IN</code>\nПримеры: US, BR, FR, DE, ID",
        "tier_premium":     "👑 УРОВЕНЬ ПРЕМИУМ",
        "tier_standard":    "⭐ СТАНДАРТНЫЙ УРОВЕНЬ",
        "tier_basic":       "🎯 БАЗОВЫЙ УРОВЕНЬ",
        "tier_prime":       "🍿 УРОВЕНЬ PRIME VIDEO",
        "stock_premium":    "👑 ПРЕМИУМ",
        "stock_standard":   "⭐ СТАНДАРТ",
        "stock_basic":      "🎯 БАЗОВЫЙ",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "tr": {
        "name": "🇹🇷 Türkçe",
        "welcome": (
            "👋 <b>HOŞ GELDİNİZ, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ 3 kademede canlı doğrulanmış Netflix çerezleri.\n"
            "Her çerez teslimattan önce kontrol edilir.\n\n"
            "📌 📌 <b>KURALLAR:</b>\n"
            "  • 📈 Saat başı kademe başına 3 çerez\n"
            "  • ⏱️ Kayan 1 saatlik pencere\n"
            "  • ❌ Ölü çerezler otomatik kaldırılır\n\n"
            "🔽 🔽 <b>HİZMET SEÇİN:</b>"
        ),
        "choose_netflix":   "🔽 <b>Netflix</b> için kademe seçin:",
        "choose_prime":     "🔽 <b>PrimeVideo</b> için kademe seçin:",
        "out_of_stock":     "❌ <b>Stok yok!</b>",
        "hourly_limit":     "⏳ Bu kademe için saatlik limite ulaştınız.",
        "cookie_delivered": "✅ <b>{tier} ÇEREZİ TESLİM EDİLDİ!</b>\n\n🔗 <code>{url}</code>\n\nÇerezi içe aktarın ve bağlantıyı açın.\nSorumlu kullanın!",
        "status_title":     "📊📊 <b>KULLANIM DURUMUNUZ</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Kullanılan: <code>{used}/3</code>\n  🔄 Kalan: <code>{left}</code>\n  📦 Stok: <code>{stock}</code>\n  🕐 Sıfırlama: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Limitler her saat kayan bazda sıfırlanır.</i>",
        "stock_title":      "📦 📦 <b>ÇEREZ STOKU</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} hesap</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>NASIL KULLANILIR</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Ana menüden kademe seçin\n"
            "2️⃣  Bot çerezin canlı olduğunu doğrular\n"
            "3️⃣  Çerezi tarayıcınıza aktarın\n"
            "4️⃣  NFToken bağlantısıyla izleyin\n\n"
            "📁 📁 <b>KADEMELER:</b>\n"
            "  👑 Premium — Tam 4K, 4 ekrana kadar\n"
            "  ⭐ Standart — 1080p HD, 2 ekrana kadar\n"
            "  🎯 Temel/Mobil — 720p, 1 ekran\n\n"
            "💡 <i>Çerezleri sorumlu kullanın.</i>"
        ),
        "select_language":  "🌐 <b>Dilinizi seçin:</b>",
        "resets_soon":      "{m}d {s}s",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Durum",
        "btn_stock":        "📦 Stok",
        "btn_help":         "ℹ️ Yardım",
        "btn_language":     "🌐 Dil",
        "btn_main_menu":    "🏠 Ana Menü",
        "btn_refresh":      "🔄 Yenile",
        "btn_by_country":   "🌍 Ülkeye Göre",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standart ({n})",
        "btn_basic":        "🎯 Temel ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 <b>{country}</b> için çerez aranıyor...",
        "country_found":    "✅ <b>{country}</b> için çerez bulundu (Demo)",
        "country_usage":    "Kullanım: <code>/country IN</code>\nÖrnekler: US, BR, FR, DE, ID",
        "tier_premium":     "👑 PREMİUM KADEME",
        "tier_standard":    "⭐ STANDART KADEME",
        "tier_basic":       "🎯 TEMEL KADEME",
        "tier_prime":       "🍿 PRIME VIDEO KADEME",
        "stock_premium":    "👑 PREMİUM",
        "stock_standard":   "⭐ STANDART",
        "stock_basic":      "🎯 TEMEL",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "de": {
        "name": "🇩🇪 Deutsch",
        "welcome": (
            "👋 <b>WILLKOMMEN, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Live-verifizierte Netflix-Cookies in 3 Stufen.\n"
            "Jeder Cookie wird vor der Lieferung geprüft.\n\n"
            "📌 📌 <b>REGELN:</b>\n"
            "  • 📈 3 Cookies pro Stufe pro Stunde\n"
            "  • ⏱️ Gleitendes 1-Stunden-Fenster\n"
            "  • ❌ Tote Cookies werden automatisch entfernt\n\n"
            "🔽 🔽 <b>DIENST WÄHLEN:</b>"
        ),
        "choose_netflix":   "🔽 Stufe für <b>Netflix</b> wählen:",
        "choose_prime":     "🔽 Stufe für <b>PrimeVideo</b> wählen:",
        "out_of_stock":     "❌ <b>Nicht vorrätig!</b>",
        "hourly_limit":     "⏳ Sie haben das Stundenlimit für diese Stufe erreicht.",
        "cookie_delivered": "✅ <b>{tier}-COOKIE GELIEFERT!</b>\n\n🔗 <code>{url}</code>\n\nCookie importieren und Link öffnen.\nVerantwortungsvoll verwenden!",
        "status_title":     "📊📊 <b>IHR NUTZUNGSSTATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Genutzt: <code>{used}/3</code>\n  🔄 Verbleibend: <code>{left}</code>\n  📦 Vorrat: <code>{stock}</code>\n  🕐 Reset: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>Limits werden stündlich rollierend zurückgesetzt.</i>",
        "stock_title":      "📦 📦 <b>COOKIE-VORRAT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} Konten</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>ANLEITUNG</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Stufe im Hauptmenü wählen\n"
            "2️⃣  Bot prüft, ob der Cookie aktiv ist\n"
            "3️⃣  Cookie im Browser importieren\n"
            "4️⃣  NFToken-Link zum Anschauen verwenden\n\n"
            "📁 📁 <b>STUFEN:</b>\n"
            "  👑 Premium — Volles 4K, bis 4 Bildschirme\n"
            "  ⭐ Standard — 1080p HD, bis 2 Bildschirme\n"
            "  🎯 Basic/Mobil — 720p, 1 Bildschirm\n\n"
            "💡 <i>Cookies verantwortungsvoll nutzen.</i>"
        ),
        "select_language":  "🌐 <b>Sprache auswählen:</b>",
        "resets_soon":      "{m}Min {s}Sek",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Status",
        "btn_stock":        "📦 Vorrat",
        "btn_help":         "ℹ️ Hilfe",
        "btn_language":     "🌐 Sprache",
        "btn_main_menu":    "🏠 Hauptmenü",
        "btn_refresh":      "🔄 Aktualisieren",
        "btn_by_country":   "🌍 Nach Land",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Basic ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Cookies für <b>{country}</b> werden gesucht...",
        "country_found":    "✅ Live-Cookies für <b>{country}</b> gefunden (Demo)",
        "country_usage":    "Verwendung: <code>/country IN</code>\nBeispiele: US, BR, FR, DE, ID",
        "tier_premium":     "👑 PREMIUM-STUFE",
        "tier_standard":    "⭐ STANDARD-STUFE",
        "tier_basic":       "🎯 BASIC-STUFE",
        "tier_prime":       "🍿 PRIME VIDEO-STUFE",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BASIC",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "it": {
        "name": "🇮🇹 Italiano",
        "welcome": (
            "👋 <b>BENVENUTO, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ Cookie Netflix verificati in tempo reale su 3 livelli.\n"
            "Ogni cookie viene verificato prima della consegna.\n\n"
            "📌 📌 <b>REGOLE:</b>\n"
            "  • 📈 3 cookie per livello all'ora\n"
            "  • ⏱️ Finestra di 1 ora scorrevole\n"
            "  • ❌ I cookie morti vengono rimossi automaticamente\n\n"
            "🔽 🔽 <b>SCEGLI UN SERVIZIO:</b>"
        ),
        "choose_netflix":   "🔽 Scegli un livello per <b>Netflix</b>:",
        "choose_prime":     "🔽 Scegli un livello per <b>PrimeVideo</b>:",
        "out_of_stock":     "❌ <b>Esaurito!</b>",
        "hourly_limit":     "⏳ Hai raggiunto il limite orario per questo livello.",
        "cookie_delivered": "✅ <b>COOKIE {tier} CONSEGNATO!</b>\n\n🔗 <code>{url}</code>\n\nImporta il cookie e apri il link.\nUsa responsabilmente!",
        "status_title":     "📊📊 <b>IL TUO STATO D'USO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 Usato: <code>{used}/3</code>\n  🔄 Rimanente: <code>{left}</code>\n  📦 Stock: <code>{stock}</code>\n  🕐 Reset: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>I limiti si resettano ogni ora in modo scorrevole.</i>",
        "stock_title":      "📦 📦 <b>STOCK COOKIE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} account</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>COME USARE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  Scegli un livello dal menu principale\n"
            "2️⃣  Il bot verifica che il cookie sia attivo\n"
            "3️⃣  Importa il cookie nel browser\n"
            "4️⃣  Usa il link NFToken per guardare\n\n"
            "📁 📁 <b>LIVELLI:</b>\n"
            "  👑 Premium — 4K completo, fino a 4 schermi\n"
            "  ⭐ Standard — 1080p HD, fino a 2 schermi\n"
            "  🎯 Base/Mobile — 720p, 1 schermo\n\n"
            "💡 <i>Usa i cookie responsabilmente.</i>"
        ),
        "select_language":  "🌐 <b>Seleziona la tua lingua:</b>",
        "resets_soon":      "{m}m {s}s",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 Stato",
        "btn_stock":        "📦 Stock",
        "btn_help":         "ℹ️ Aiuto",
        "btn_language":     "🌐 Lingua",
        "btn_main_menu":    "🏠 Menu Principale",
        "btn_refresh":      "🔄 Aggiorna",
        "btn_by_country":   "🌍 Per Paese",
        "btn_premium":      "👑 Premium ({n})",
        "btn_standard":     "⭐ Standard ({n})",
        "btn_basic":        "🎯 Base ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 Ricerca cookie per: <b>{country}</b>...",
        "country_found":    "✅ Cookie trovati per <b>{country}</b> (Demo)",
        "country_usage":    "Uso: <code>/country IN</code>\nEsempi: US, BR, FR, DE, ID",
        "tier_premium":     "👑 LIVELLO PREMIUM",
        "tier_standard":    "⭐ LIVELLO STANDARD",
        "tier_basic":       "🎯 LIVELLO BASE",
        "tier_prime":       "🍿 LIVELLO PRIME VIDEO",
        "stock_premium":    "👑 PREMIUM",
        "stock_standard":   "⭐ STANDARD",
        "stock_basic":      "🎯 BASE",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "ja": {
        "name": "🇯🇵 日本語",
        "welcome": (
            "👋 <b>ようこそ、CAY！</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ 3段階でリアルタイム検証済みのNetflixクッキー。\n"
            "すべてのクッキーは配信前に確認されます。\n\n"
            "📌 📌 <b>ルール：</b>\n"
            "  • 📈 1段階あたり1時間に3クッキー\n"
            "  • ⏱️ ローリング1時間ウィンドウ\n"
            "  • ❌ 無効なクッキーは自動削除\n\n"
            "🔽 🔽 <b>サービスを選択：</b>"
        ),
        "choose_netflix":   "🔽 <b>Netflix</b> の段階を選択：",
        "choose_prime":     "🔽 <b>PrimeVideo</b> の段階を選択：",
        "out_of_stock":     "❌ <b>在庫切れ！</b>",
        "hourly_limit":     "⏳ この段階の1時間制限に達しました。",
        "cookie_delivered": "✅ <b>{tier} クッキーが配信されました！</b>\n\n🔗 <code>{url}</code>\n\nクッキーをインポートしてリンクを開いてください。\n責任ある使用をお願いします！",
        "status_title":     "📊📊 <b>利用状況</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 使用済み: <code>{used}/3</code>\n  🔄 残り: <code>{left}</code>\n  📦 在庫: <code>{stock}</code>\n  🕐 リセット: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>制限は1時間ごとにローリングでリセットされます。</i>",
        "stock_title":      "📦 📦 <b>クッキー在庫</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} アカウント</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>使い方</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  メインメニューから段階を選択\n"
            "2️⃣  ボットがクッキーの有効性を確認\n"
            "3️⃣  ブラウザにクッキーをインポート\n"
            "4️⃣  NFTokenリンクで視聴\n\n"
            "📁 📁 <b>段階：</b>\n"
            "  👑 プレミアム — フル4K、最大4画面\n"
            "  ⭐ スタンダード — 1080p HD、最大2画面\n"
            "  🎯 ベーシック/モバイル — 720p、1画面\n\n"
            "💡 <i>クッキーは責任ある使用をお願いします。</i>"
        ),
        "select_language":  "🌐 <b>言語を選択：</b>",
        "resets_soon":      "{m}分 {s}秒",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 ステータス",
        "btn_stock":        "📦 在庫",
        "btn_help":         "ℹ️ ヘルプ",
        "btn_language":     "🌐 言語",
        "btn_main_menu":    "🏠 メインメニュー",
        "btn_refresh":      "🔄 更新",
        "btn_by_country":   "🌍 国別",
        "btn_premium":      "👑 プレミアム ({n})",
        "btn_standard":     "⭐ スタンダード ({n})",
        "btn_basic":        "🎯 ベーシック ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 <b>{country}</b> のクッキーを検索中...",
        "country_found":    "✅ <b>{country}</b> のライブクッキーが見つかりました（デモ）",
        "country_usage":    "使用法: <code>/country IN</code>\n例: US, BR, FR, DE, ID",
        "tier_premium":     "👑 プレミアム段階",
        "tier_standard":    "⭐ スタンダード段階",
        "tier_basic":       "🎯 ベーシック段階",
        "tier_prime":       "🍿 PRIME VIDEO段階",
        "stock_premium":    "👑 プレミアム",
        "stock_standard":   "⭐ スタンダード",
        "stock_basic":      "🎯 ベーシック",
        "stock_prime":      "🍿 PRIME VIDEO",
    },

    "ko": {
        "name": "🇰🇷 한국어",
        "welcome": (
            "👋 <b>환영합니다, CAY!</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚡ 3가지 등급의 실시간 인증 Netflix 쿠키.\n"
            "모든 쿠키는 배달 전에 확인됩니다.\n\n"
            "📌 📌 <b>규칙:</b>\n"
            "  • 📈 등급당 시간당 3개 쿠키\n"
            "  • ⏱️ 롤링 1시간 윈도우\n"
            "  • ❌ 죽은 쿠키는 자동 제거\n\n"
            "🔽 🔽 <b>서비스 선택:</b>"
        ),
        "choose_netflix":   "🔽 <b>Netflix</b> 등급 선택:",
        "choose_prime":     "🔽 <b>PrimeVideo</b> 등급 선택:",
        "out_of_stock":     "❌ <b>재고 없음!</b>",
        "hourly_limit":     "⏳ 이 등급의 시간당 제한에 도달했습니다.",
        "cookie_delivered": "✅ <b>{tier} 쿠키 배달 완료!</b>\n\n🔗 <code>{url}</code>\n\n쿠키를 가져오고 링크를 여세요.\n책임감 있게 사용하세요!",
        "status_title":     "📊📊 <b>사용 현황</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "status_tier":      "<b>{name}</b>\n  📈 사용: <code>{used}/3</code>\n  🔄 남은: <code>{left}</code>\n  📦 재고: <code>{stock}</code>\n  🕐 초기화: <code>{resets}</code>\n\n",
        "status_footer":    "💡 <i>제한은 매시간 롤링 방식으로 초기화됩니다.</i>",
        "stock_title":      "📦 📦 <b>쿠키 재고</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
        "stock_row":        "<b>{name}:</b> <code>{count} 계정</code>\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩\n\n",
        "help_text": (
            "ℹ️ ℹ️ <b>사용 방법</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣  메인 메뉴에서 등급 선택\n"
            "2️⃣  봇이 쿠키가 활성 상태인지 확인\n"
            "3️⃣  브라우저에 쿠키 가져오기\n"
            "4️⃣  NFToken 링크로 시청\n\n"
            "📁 📁 <b>등급:</b>\n"
            "  👑 프리미엄 — 풀 4K, 최대 4개 화면\n"
            "  ⭐ 스탠다드 — 1080p HD, 최대 2개 화면\n"
            "  🎯 베이직/모바일 — 720p, 1개 화면\n\n"
            "💡 <i>쿠키를 책임감 있게 사용하세요.</i>"
        ),
        "select_language":  "🌐 <b>언어 선택:</b>",
        "resets_soon":      "{m}분 {s}초",
        "resets_none":      "—",
        "btn_netflix":      "🎬 Netflix",
        "btn_prime":        "🍿 Prime Video",
        "btn_status":       "📊 상태",
        "btn_stock":        "📦 재고",
        "btn_help":         "ℹ️ 도움말",
        "btn_language":     "🌐 언어",
        "btn_main_menu":    "🏠 메인 메뉴",
        "btn_refresh":      "🔄 새로고침",
        "btn_by_country":   "🌍 국가별",
        "btn_premium":      "👑 프리미엄 ({n})",
        "btn_standard":     "⭐ 스탠다드 ({n})",
        "btn_basic":        "🎯 베이직 ({n})",
        "btn_prime_video":  "🍿 Prime Video ({n})",
        "country_searching":"🔍 <b>{country}</b> 의 쿠키 검색 중...",
        "country_found":    "✅ <b>{country}</b> 의 쿠키를 찾았습니다 (데모)",
        "country_usage":    "사용법: <code>/country IN</code>\n예시: US, BR, FR, DE, ID",
        "tier_premium":     "👑 프리미엄 등급",
        "tier_standard":    "⭐ 스탠다드 등급",
        "tier_basic":       "🎯 베이직 등급",
        "tier_prime":       "🍿 PRIME VIDEO 등급",
        "stock_premium":    "👑 프리미엄",
        "stock_standard":   "⭐ 스탠다드",
        "stock_basic":      "🎯 베이직",
        "stock_prime":      "🍿 PRIME VIDEO",
    },
}

# ====================== HELPERS ======================
DEFAULT_LANG = "en"

def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Fetch a translated string for the given lang and key.
    Falls back to English if the lang or key is missing.
    Supports format placeholders: get_text("es", "cookie_delivered", tier="PREMIUM", url="...")
    """
    strings = LANGUAGES.get(lang) or LANGUAGES[DEFAULT_LANG]
    template = strings.get(key) or LANGUAGES[DEFAULT_LANG].get(key, f"[{key}]")
    return template.format(**kwargs) if kwargs else template

def get_lang_name(lang: str) -> str:
    """Return the display name of a language code, e.g. 'en' → '🇬🇧 English'"""
    return LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG])["name"]

def supported_langs() -> list[str]:
    """Return all supported language codes."""
    return list(LANGUAGES.keys())