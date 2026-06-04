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

# ☠️ PSPAM DATABASE COLLECTION ☠️
pspam_db = db["pspam_ammo"] if db is not None else None

# 🧠 IN-MEMORY STATES
ADD_PSPAM_STATE = {}
SPAM_RUNNING = {} # 🔥 Naya Switch Spam Rokne Ke Liye

# ==========================================
# 🛡️ ꜱᴜᴅᴏ ᴄʜᴇᴄᴋᴇʀ ꜰᴜɴᴄᴛɪᴏɴ 
# ==========================================
async def check_sudo(user_id):
    if user_id == OWNER_ID:
        return True
    return await database.is_sudo_db(user_id)

# ==========================================
# ⚡ ADVANCED PARALLEL EXECUTION ENGINE (SMART BYPASS)
# ==========================================
async def fire_message(client, chat_id, text):
    try:
        await client.send_message(chat_id, text)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except (ChatWriteForbidden, UserRestricted):
        SPAM_RUNNING[chat_id] = False # 🔥 Smart Mute Detection (Admin bypass)
    except Exception:
        pass

async def fire_copy(client, chat_id, message_id):
    try:
        await client.copy_message(chat_id, chat_id, message_id)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except (ChatWriteForbidden, UserRestricted):
        SPAM_RUNNING[chat_id] = False # 🔥 Smart Mute Detection (Admin bypass)
    except Exception:
        pass

async def fire_media(client, chat_id, media_type, file_id):
    try:
        if media_type == "photo": await client.send_photo(chat_id, file_id)
        elif media_type == "video": await client.send_video(chat_id, file_id)
        elif media_type == "sticker": await client.send_sticker(chat_id, file_id)
        elif media_type == "animation": await client.send_animation(chat_id, file_id)
        elif media_type == "document": await client.send_document(chat_id, file_id)
    except FloodWait as fw:
        await asyncio.sleep(fw.value)
    except (ChatWriteForbidden, UserRestricted):
        SPAM_RUNNING[chat_id] = False # 🔥 Smart Media Restrict Detection
    except Exception:
        pass

# ==========================================
# 🛑 EMERGENCY BRAKES COMMAND (/stopspam & /stoppspam)
# ==========================================
@Client.on_message(filters.command(["stopspam", "stoppspam"]))
async def stop_spam_cmd(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_DEVIL} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    if SPAM_RUNNING.get(chat_id, False):
        SPAM_RUNNING[chat_id] = False
        await message.reply_text(f"<blockquote>{E_STOP} <b>ꜱ ᴘ ᴀ ᴍ  ꜱ ᴛ ᴏ ᴘ ᴘ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text(f"<blockquote>{E_WARN} <b>ᴋ ᴏ ɪ  ꜱ ᴘ ᴀ ᴍ  ɴ ᴀ ʜ ɪ ɴ  ᴄ ʜ ᴀ ʟ  ʀ ᴀ ʜ ᴀ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)


# ==========================================
# ☢️ 1. NORMAL SPAM COMMAND (/spam)
# ==========================================
@Client.on_message(filters.command("spam"))
async def normal_spam(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_DEVIL} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/spam 10 text</code> ᴏ ʀ  ʀ ᴇ ᴘ ʟ ʏ  ᴛ ᴏ  ᴍ ᴇ ꜱ ꜱ ᴀ ɢ ᴇ .</blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        count = int(message.command[1])
    except:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ᴀ ʙ ᴇ  ɴ ᴀ ʟ ʟ ᴇ ,  ᴄ ᴏ ᴜ ɴ ᴛ  ɴ ᴜ ᴍ ʙ ᴇ ʀ  ᴍ ᴇɪ ɴ  ᴅ ᴀ ʟ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    SPAM_RUNNING[chat_id] = True # 🔥 Switch ON

    if message.reply_to_message:
        msg_id = message.reply_to_message.id
        for _ in range(count):
            if not SPAM_RUNNING.get(chat_id, False): break
            asyncio.create_task(fire_copy(client, chat_id, msg_id))
            await asyncio.sleep(0.05) # Micro-delay for stop command checking
    else:
        text = message.text.split(None, 2)[2]
        for _ in range(count):
            if not SPAM_RUNNING.get(chat_id, False): break
            asyncio.create_task(fire_message(client, chat_id, text))
            await asyncio.sleep(0.05)

    SPAM_RUNNING[chat_id] = False # Auto Switch OFF after loop


# ==========================================
# ☢️ 2. PSPAM AMMO LOADER (/addpspam)
# ==========================================
@Client.on_message(filters.command("addpspam"))
async def toggle_pspam_loader(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if pspam_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)
        
    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/addpspam on/off/clear</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    state = message.command[1].lower()

    if state == "on":
        ADD_PSPAM_STATE[user_id] = True
        await message.reply_text(f"<blockquote>{E_CHECK} <b>ᴘ ꜱ ᴘ ᴀ ᴍ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴀ ᴄ ᴛ ɪ ᴠ ᴀ ᴛ ᴇ ᴅ !</b>\nꜱ ᴇ ɴ ᴅ  ᴀ ʟ ʟ  ᴍ ᴇ ᴅ ɪ ᴀ  ɴ ᴏ ᴡ . 🤫</blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "off":
        ADD_PSPAM_STATE[user_id] = False
        count = await pspam_db.count_documents({})
        await message.reply_text(f"<blockquote>{E_FLASH} <b>ᴘ ꜱ ᴘ ᴀ ᴍ  ʟ ᴏ ᴀ ᴅ ᴇ ʀ  ᴏ ꜰ ꜰ !</b>\nᴛ ᴏ ᴛ ᴀ ʟ  ᴀ ᴍ ᴍ ᴏ : <b>{count}</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    elif state == "clear":
        await pspam_db.delete_many({})
        await message.reply_text(f"<blockquote>{E_CHECK} ᴀ ʟ ʟ  ᴀ ᴍ ᴍ ᴏ  ᴄ ʟ ᴇ ᴀ ʀ ᴇ ᴅ !</blockquote>", parse_mode=enums.ParseMode.HTML)


# ==========================================
# 🧲 3. STEALTH MEDIA CATCHER (ZERO-REPLY)
# ==========================================
@Client.on_message(
    (filters.photo | filters.video | filters.animation | filters.sticker | filters.document)
)
async def stealth_media_catcher(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not ADD_PSPAM_STATE.get(user_id, False) or pspam_db is None:
        return
    if not await check_sudo(user_id):
        return

    file_id, media_type = None, None

    if message.photo: file_id, media_type = message.photo.file_id, "photo"
    elif message.video: file_id, media_type = message.video.file_id, "video"
    elif message.animation: file_id, media_type = message.animation.file_id, "animation"
    elif message.sticker: file_id, media_type = message.sticker.file_id, "sticker"
    elif message.document: file_id, media_type = message.document.file_id, "document"

    if file_id and media_type:
        await pspam_db.insert_one({"file_id": file_id, "type": media_type})


# ==========================================
# ☢️ 4. PREMIUM SPAM COMMAND (/pspam)
# ==========================================
@Client.on_message(filters.command("pspam"))
async def premium_spam(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_CROWN} <b>ʙ ᴀ ᴀ ᴘ  ꜱ ᴇ  ꜱ ᴜ ᴅ ᴏ  ʟ ᴇ  ᴘ ᴇ ʜ ʟ ᴇ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if pspam_db is None:
        return await message.reply_text(f"<blockquote>{E_WARN} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ʀ ʀ ᴏ ʀ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/pspam 10</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        count = int(message.command[1])
    except:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ɪ ɴ ᴠ ᴀ ʟ ɪ ᴅ  ᴄ ᴏ ᴜ ɴ ᴛ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    all_ammo = await pspam_db.find().to_list(length=None)
    
    if not all_ammo:
        return await message.reply_text(f"<blockquote>{E_DEVIL} ᴅ ᴀ ᴛ ᴀ ʙ ᴀ ꜱ ᴇ  ᴇ ᴍ ᴘ ᴛ ʏ !  ᴘ ᴇ ʜ ʟ ᴇ  <code>/addpspam on</code>  ᴋ ᴀ ʀ ᴋ ᴇ  ᴍ ᴀ ᴀ ʟ  ᴅ ᴀ ʟ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    chat_id = message.chat.id
    SPAM_RUNNING[chat_id] = True # 🔥 Switch ON

    for _ in range(count):
        if not SPAM_RUNNING.get(chat_id, False): break # Check brake
        random_media = random.choice(all_ammo)
        asyncio.create_task(fire_media(client, chat_id, random_media["type"], random_media["file_id"]))
        await asyncio.sleep(0.05) # Micro-delay for stop command checking

    SPAM_RUNNING[chat_id] = False # Auto Switch OFF after loop
