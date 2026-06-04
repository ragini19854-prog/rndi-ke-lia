import asyncio
import random
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, ChatWriteForbidden, UserRestricted

# ☠️ MONSTER MULTI-BOTS IMPORTS 
from core import database
from config import OWNER_ID
from core.database import db 

# ==========================================
# 💎 ʏᴜᴋɪ'ꜱ ᴘʀᴇᴍɪᴜᴍ ᴇᴍᴏᴊɪ ᴠᴀᴜʟᴛ
# ==========================================
E_DEVIL = "<emoji id='6199535419168659446'>☠</emoji>"
E_CROWN = "<emoji id='6118612596019958861'>👑</emoji>"
E_WARN  = "<emoji id='5188463524568926712'>⚠️</emoji>"
E_CHECK = "<emoji id='5431757423134121353'>✅</emoji>"
E_FLASH = "<emoji id='5345905193005371012'>⚡️</emoji>"
E_LOCK  = "<emoji id='6115973347206501819'>🔒</emoji>"
E_STOP  = "<emoji id='6131813839429177098'>🚫</emoji>"

# ☠️ SRAID DATABASE COLLECTION (Naya Table) ☠️
sraid_db = db["sraid_ammo"] if db is not None else None

# 🧠 IN-MEMORY STATES
ADD_SRAID_STATE = {}
SRAID_RUNNING = {} # 🔥 Emergency Brake Switch

# ==========================================
# 🛡️ ꜱᴜᴅᴏ ᴄʜᴇᴄᴋᴇʀ ꜰᴜɴᴄᴛɪᴏɴ 
# ==========================================
async def check_sudo(user_id):
    if user_id == OWNER_ID:
        return True
    return await database.is_sudo_db(user_id)

# ==========================================
# ⚡ SRAID PARALLEL EXECUTION ENGINE (SMART BYPASS)
# ==========================================
async def fire_sraid(client, chat_id, text):
    try:
        await client.send_message(chat_id, text)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except (ChatWriteForbidden, UserRestricted):
        SRAID_RUNNING[chat_id] = False # 🔥 Smart Mute Detection (Admin bypass)
    except Exception:
        pass

# ==========================================
# 🛑 EMERGENCY BRAKES COMMAND (/stopsraid)
# ==========================================
@Client.on_message(filters.command(["stopsraid"]))
async def stop_sraid_cmd(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_DEVIL} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    if SRAID_RUNNING.get(chat_id, False):
        SRAID_RUNNING[chat_id] = False
        await message.reply_text(f"<blockquote>{E_STOP} <b>ꜱ ʀ ᴀ ɪ ᴅ  ꜱ ᴛ ᴏ ᴘ ᴘ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text(f"<blockquote>{E_WARN} <b>ᴋ ᴏ ɪ  ꜱ ʀ ᴀ ɪ ᴅ  ɴ ᴀ ʜ ɪ ɴ  ᴄ ʜ ᴀ ʟ  ʀ ᴀ ʜ ɪ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 1. SRAID AMMO LOADER (/addsraid)
# ==========================================
@Client.on_message(filters.command("addsraid"))
async def toggle_sraid_loader(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if sraid_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)
        
    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/addsraid on/off/clear</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    state = message.command[1].lower()

    if state == "on":
        ADD_SRAID_STATE[user_id] = True
        await message.reply_text(f"<blockquote>{E_CHECK} <b>ꜱ ʀ ᴀ ɪ ᴅ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴀ ᴄ ᴛ ɪ ᴠ ᴀ ᴛ ᴇ ᴅ !</b>\nꜱ ᴇ ɴ ᴅ  ᴀ ʟ ʟ  ꜱ ʜ ᴀ ʏ ᴀ ʀ ɪ / ᴛ ᴇ x ᴛ  ɴ ᴏ ᴡ . 🤫</blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "off":
        ADD_SRAID_STATE[user_id] = False
        count = await sraid_db.count_documents({})
        await message.reply_text(f"<blockquote>{E_FLASH} <b>ꜱ ʀ ᴀ ɪ ᴅ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴏ ꜰ ꜰ !</b>\nᴛ ᴏ ᴛ ᴀ ʟ  ᴀ ᴍ ᴍ ᴏ : <b>{count}</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "clear":
        await sraid_db.delete_many({})
        await message.reply_text(f"<blockquote>{E_CHECK} ᴀ ʟ ʟ  ꜱ ʀ ᴀ ɪ ᴅ  ᴀ ᴍ ᴍ ᴏ  ᴄ ʟ ᴇ ᴀ ʀ ᴇ ᴅ !</blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# 🧲 2. STEALTH TEXT CATCHER (ZERO-REPLY)
# ==========================================
@Client.on_message(filters.text & ~filters.command(["addsraid", "sraid", "stopsraid", "spam", "pspam"]))
async def stealth_sraid_catcher(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not ADD_SRAID_STATE.get(user_id, False) or sraid_db is None:
        return
    if not await check_sudo(user_id):
        return

    # Text ko silently DB mein save karega
    text_ammo = message.text
    if text_ammo:
        await sraid_db.insert_one({"text": text_ammo})

# ==========================================
# ☢️ 3. SRAID COMMAND (/sraid)
# ==========================================
@Client.on_message(filters.command("sraid"))
async def sraid_spam(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_CROWN} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if sraid_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/sraid 10</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        count = int(message.command[1])
    except:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ɪ ɴ ᴠ ᴀ ʟ ɪ ᴅ  ᴄ ᴏ ᴜ ɴ ᴛ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    # 🎲 Fetch all text ammo from DB
    all_ammo = await sraid_db.find().to_list(length=None)
    
    if not all_ammo:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ᴍ ᴘ ᴛ ʏ !  ᴘ ᴇ ʜ ʟ ᴇ  <code>/addsraid on</code>  ᴋ ᴀ ʀ ᴋ ᴇ  ᴍ ᴀ ᴀ ʟ  ᴅ ᴀ ʟ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    SRAID_RUNNING[chat_id] = True # 🔥 Switch ON

    for _ in range(count):
        if not SRAID_RUNNING.get(chat_id, False): break # Check brake
        random_shayari = random.choice(all_ammo)["text"]
        asyncio.create_task(fire_sraid(client, chat_id, random_shayari))
        await asyncio.sleep(0.05) # Micro-delay for stop command checking

    SRAID_RUNNING[chat_id] = False # Auto Switch OFF after loop
