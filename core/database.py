from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient
from pymongo.errors import ServerSelectionTimeoutError
from config import MONGO_DB_URI, LOGGER

# ==========================================
# ⚡ MONGODB CLIENT SETUP WITH TIMEOUT
# ==========================================
# Agar 5 second me connect nahi hua to hang nahi hoga, error de dega
try:
    if MONGO_DB_URI:
        LOGGER.info("⚡ Connecting to MongoDB Matrix...")
        mongo: AgnosticClient = AsyncIOMotorClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        db = mongo["YUKI_MULTI_MATRIX"]
        
        # 🗃️ Collections (Tables)
        usersdb = db["users"]
        sudoersdb = db["sudoers"]
        blacklistdb = db["blacklist"]
        
        LOGGER.info("✅ MongoDB Matrix Connected & Synced!")
    else:
        db = None
        usersdb = sudoersdb = blacklistdb = None
        LOGGER.warning("⚠️ MONGO_DB_URI NOT FOUND! DB Features Disabled.")
except Exception as e:
    LOGGER.error(f"💀 MongoDB Connection Failed: {e}")
    db = None


# ==========================================
# 🛠️ MATRIX DB HELPER FUNCTIONS (Pro-Level)
# ==========================================

# 👤 USERS LOGIC
async def is_user(user_id: int) -> bool:
    if usersdb is None: return False
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

async def add_user(user_id: int):
    if usersdb is None: return
    if not await is_user(user_id):
        await usersdb.insert_one({"user_id": user_id})

# 👑 SUDO LOGIC
async def is_sudo_db(user_id: int) -> bool:
    if sudoersdb is None: return False
    user = await sudoersdb.find_one({"user_id": user_id})
    return bool(user)

async def add_sudo_db(user_id: int):
    if sudoersdb is None: return
    if not await is_sudo_db(user_id):
        await sudoersdb.insert_one({"user_id": user_id})
        
async def get_all_sudoers():
    if sudoersdb is None: return []
    sudoers = await sudoersdb.find().to_list(length=None)
    return [x["user_id"] for x in sudoers]

# 🚫 BLACKLIST (BANNED USERS) LOGIC
async def is_banned(user_id: int) -> bool:
    if blacklistdb is None: return False
    user = await blacklistdb.find_one({"user_id": user_id})
    return bool(user)

async def ban_user(user_id: int):
    if blacklistdb is None: return
    if not await is_banned(user_id):
        await blacklistdb.insert_one({"user_id": user_id})

async def unban_user(user_id: int):
    if blacklistdb is None: return
    await blacklistdb.delete_one({"user_id": user_id})
