import os
import logging
from dotenv import load_dotenv

# ⚡ MADARA MATRIX ULTIMATE CONFIG ENGINE ⚡
load_dotenv()

# ==========================================
# 📝 LOGGING SETUP (CLEAN TERMINAL)
# ==========================================
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("matrix.log"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger("YUKI_MATRIX")

# ==========================================
# ☠️ CORE CREDENTIALS
# ==========================================
API_ID = int(os.getenv("API_ID", "36522229"))
API_HASH = os.getenv("API_HASH", "7f27443617af60bcb0e23f7147d3eaf9")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://bsdk:betichod@cluster0.fgj1r9z.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(os.getenv("OWNER_ID", "6670240589"))

# ==========================================
# 👑 PERMISSIONS & CONTROL (SUDO & BLACKLIST)
# ==========================================
# 1. SUDO USERS LOGIC
SUDO_USERS = [OWNER_ID]
sudo_env = os.getenv("SUDO_USERS", "")
if sudo_env:
    # List comprehension se clean code
    SUDO_USERS.extend([int(x) for x in sudo_env.split() if x.isdigit()])
SUDO_USERS = list(set(SUDO_USERS)) # Duplicate IDs hata dega

# 2. BLACKLIST USERS LOGIC (Naya add kiya)
BLACKLIST_USERS = []
bl_env = os.getenv("BLACKLIST_USERS", "")
if bl_env:
    BLACKLIST_USERS.extend([int(x) for x in bl_env.split() if x.isdigit()])
BLACKLIST_USERS = list(set(BLACKLIST_USERS))

# ==========================================
# ⚙️ ADVANCED SYSTEM SETTINGS
# ==========================================
# Log Group ID (Agar di hai toh int me convert karega)
log_env = os.getenv("LOG_GROUP_ID", "")
LOG_GROUP_ID = int(log_env) if log_env.lstrip("-").isdigit() else None

# Command Prefixes (List me convert karega: ['/', '.', '!'])
COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "/ . !").split()

# Pyrogram Workers (Quantum Speed ke liye)
WORKERS = int(os.getenv("WORKERS", "32"))

# Default Start/Alive Image
ALIVE_IMG = os.getenv("ALIVE_IMG", "https://i.ibb.co/YFf0FKw3/CTELBTl-F.jpg")

# ==========================================
# 💣 DESTRUCTION / SPAM SETTINGS
# ==========================================
DEFAULT_SPAM_DELAY = float(os.getenv("DEFAULT_SPAM_DELAY", "0.5"))
MAX_SPAM_LIMIT = int(os.getenv("MAX_SPAM_LIMIT", "1000"))

# ==========================================
# 🤖 DYNAMIC MATRIX NODES (BOT TOKENS)
# ==========================================
BOT_TOKENS = []
for i in range(1, 21):
    token = os.getenv(f"BOT_TOKEN_{i}")
    # Basic check takii galat token load na ho
    if token and ":" in token: 
        BOT_TOKENS.append(token)

if not BOT_TOKENS:
    LOGGER.error("❌ NO BOT TOKENS FOUND IN .env! SYSTEM HALTED.")
    exit()
else:
    LOGGER.info(f"✅ {len(BOT_TOKENS)} Bots Loaded | {len(SUDO_USERS)} SUDO | {len(BLACKLIST_USERS)} BANNED.")
