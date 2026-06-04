import asyncio
import random
import re
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

# ☠️ RAID DATABASE COLLECTION (Naya Table) ☠️
raid_db = db["raid_ammo"] if db is not None else None

# 🧠 IN-MEMORY STATES
ADD_RAID_STATE = {}
RAID_RUNNING = {} 

# ==========================================
# 🛡️ ꜱᴜᴅᴏ & ᴏᴡɴᴇʀ ᴄʜᴇᴄᴋᴇʀ ꜰᴜɴᴄᴛɪᴏɴ 
# ==========================================
async def check_sudo(user_id):
    if user_id == OWNER_ID:
        return True
    return await database.is_sudo_db(user_id)

# ==========================================
# 🧠 CUSTOM FILTER (Saves CPU & unblocks other commands)
# ==========================================
async def check_raid_state(_, client, message):
    user_id = message.from_user.id if message.from_user else 0
    return ADD_RAID_STATE.get(user_id, False)

raid_state_filter = filters.create(check_raid_state)

# ==========================================
# ⚡ RAID PARALLEL EXECUTION ENGINE (SMART BYPASS)
# ==========================================
async def fire_raid(client, chat_id, text):
    try:
        await client.send_message(chat_id, text, parse_mode=enums.ParseMode.HTML)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except (ChatWriteForbidden, UserRestricted):
        RAID_RUNNING[chat_id] = False 
    except Exception:
        pass

# ==========================================
# 🛑 EMERGENCY BRAKES COMMAND (/stopraid) - SUDO & OWNER
# ==========================================
@Client.on_message(filters.command(["stopraid"]))
async def stop_raid_cmd(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_DEVIL} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    if RAID_RUNNING.get(chat_id, False):
        RAID_RUNNING[chat_id] = False
        await message.reply_text(f"<blockquote>{E_STOP} <b>ʀ ᴀ ɪ ᴅ  ꜱ ᴛ ᴏ ᴘ ᴘ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text(f"<blockquote>{E_WARN} <b>ᴋ ᴏ ɪ  ʀ ᴀ ɪ ᴅ  ɴ ᴀ ʜ ɪ ɴ  ᴄ ʜ ᴀ ʟ  ʀ ᴀ ʜ ɪ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 1. RAID AMMO LOADER (/addraid) - ONLY OWNER
# ==========================================
@Client.on_message(filters.command("addraid"))
async def toggle_raid_loader(client, message):
    user_id = message.from_user.id if message.from_user else 0
    
    # 🔥 Sirf aur sirf Owner check!
    if user_id != OWNER_ID:
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʏ ᴇ ʜ  ᴘ ᴏ ᴡ ᴇ ʀ  ꜱ ɪ ʀ ꜰ  ᴏ ᴡ ɴ ᴇ ʀ  ᴋ ᴇ  ᴘ ᴀ ᴀ ꜱ  ʜ ᴀ ɪ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if raid_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)
        
    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/addraid on/off/clear</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    state = message.command[1].lower()

    if state == "on":
        ADD_RAID_STATE[user_id] = True
        await message.reply_text(f"<blockquote>{E_CHECK} <b>ʀ ᴀ ɪ ᴅ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴀ ᴄ ᴛ ɪ ᴠ ᴀ ᴛ ᴇ ᴅ !</b>\nꜱ ᴇ ɴ ᴅ  ᴀ ʟ ʟ  ᴛ ᴇ x ᴛ / ᴍ ꜱ ɢ ꜱ  ɴ ᴏ ᴡ . 🤫</blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "off":
        ADD_RAID_STATE[user_id] = False
        count = await raid_db.count_documents({})
        await message.reply_text(f"<blockquote>{E_FLASH} <b><b>ʀ ᴀ ɪ ᴅ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴏ ꜰ ꜰ !</b></b>\nᴛ ᴏ ᴛ ᴀ ʟ  ᴀ ᴍ ᴍ ᴏ : <b>{count}</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "clear":
        await raid_db.delete_many({})
        await message.reply_text(f"<blockquote>{E_CHECK} ᴀ ʟ ʟ  ʀ ᴀ ɪ ᴅ  ᴀ ᴍ ᴍ ᴏ  ᴄ ʟ ᴇ ᴀ ʀ ᴇ ᴅ !</blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# 🧲 2. ADVANCED LINE SPLITTER CATCHER (ZERO-REPLY) - ONLY OWNER
# ==========================================
@Client.on_message(filters.text & raid_state_filter)
async def stealth_raid_catcher(client, message):
    user_id = message.from_user.id if message.from_user else 0
    
    # 🔥 Sirf Owner text save kar sakta hai
    if user_id != OWNER_ID:
        return

    # 🛑 COMMAND BLOCKER
    if message.text.startswith(("/", "!", ".")):
        return

    # 🔥 Bulk Text Split Logic
    raw_text = message.text
    lines = raw_text.split('\n')
    
    ammo_to_insert = []
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            clean_line = re.sub(r'^\d+\s*\.\s*', '', clean_line).strip()
            if clean_line:
                ammo_to_insert.append({"text": clean_line})

    if ammo_to_insert:
        if len(ammo_to_insert) == 1:
            await raid_db.insert_one(ammo_to_insert[0])
        else:
            await raid_db.insert_many(ammo_to_insert)

# ==========================================
# ☢️ 3. TARGETED RAID COMMAND (/raid) - SUDO & OWNER
# ==========================================
@Client.on_message(filters.command("raid"))
async def raid_spam(client, message):
    user_id = message.from_user.id if message.from_user else 0
    
    # 🎯 Sudo Check yahan bhi laga hai!
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_CROWN} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if raid_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    args = message.command
    target_user = None
    count = 0

    # 🎯 TARGET DETECTION (Reply vs Username/ID)
    if message.reply_to_message:
        if len(args) < 2:
            return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/raid 10</code> (ᴏ ɴ  ʀ ᴇ ᴘ ʟ ʏ)</blockquote>", parse_mode=enums.ParseMode.HTML)
        try:
            count = int(args[1])
            target_user = message.reply_to_message.from_user
        except:
            return await message.reply_text(f"<blockquote>{E_DEVIL} ɪ ɴ ᴠ ᴀ ʟ ɪ ᴅ  ᴄ ᴏ ᴜ ɴ ᴛ !</blockquote>", parse_mode=enums.ParseMode.HTML)
    else:
        if len(args) < 3:
            return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/raid 10 @username</code></blockquote>", parse_mode=enums.ParseMode.HTML)
        try:
            count = int(args[1])
            target = args[2]
            target_user = await client.get_users(target)
        except Exception:
            return await message.reply_text(f"<blockquote>{E_DEVIL} ᴜ ꜱ ᴇ ʀ  ɴ ᴀ ʜ ɪ ɴ  ᴍ ɪ ʟ ᴀ ! ꜱ ᴀ ʜ ɪ  ɪ ᴅ / ᴜ ꜱ ᴇ ʀ ɴ ᴀ ᴍ ᴇ  ᴅ ᴀ ʟ .</blockquote>", parse_mode=enums.ParseMode.HTML)

    if not target_user:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ᴜ ꜱ ᴇ ʀ  ꜰ ᴏ ᴜ ɴ ᴅ  ɴ ᴀ ʜ ɪ ɴ  ʜ ᴜ ᴀ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    all_ammo = await raid_db.find().to_list(length=None)
    
    if not all_ammo:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ᴍ ᴘ ᴛ ʏ !  ᴘ ᴇ ʜ ʟ ᴇ  <code>/addraid on</code>  ᴋ ᴀ ʀ ᴋ ᴇ  ᴍ ᴀ ᴀ ʟ  ᴅ ᴀ ʟ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    RAID_RUNNING[chat_id] = True 

    # 🧲 Generate Target Mention
    user_mention = f"<a href='tg://user?id={target_user.id}'>{target_user.first_name}</a>"

    for _ in range(count):
        if not RAID_RUNNING.get(chat_id, False): break 
        random_text = random.choice(all_ammo)["text"]
        
        final_text = f"{user_mention} {random_text}"
        asyncio.create_task(fire_raid(client, chat_id, final_text))
        await asyncio.sleep(0.05) 

    RAID_RUNNING[chat_id] = False 
