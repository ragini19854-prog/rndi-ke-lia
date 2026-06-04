import os
import asyncio
import urllib.request
import urllib.parse
import json
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait

# ☠️ MONSTER MULTI-BOTS IMPORTS 
from core import database
from config import OWNER_ID

# ==========================================
# 💎 ʏᴜᴋɪ'ꜱ ᴘʀᴇᴍɪᴜᴍ ᴇᴍᴏᴊɪ ᴠᴀᴜʟᴛ
# ==========================================
E_DEVIL = "<emoji id='6199535419168659446'>☠</emoji>"
E_CROWN = "<emoji id='6118612596019958861'>👑</emoji>"
E_WARN  = "<emoji id='5188463524568926712'>⚠️</emoji>"
E_CHECK = "<emoji id='5431757423134121353'>✅</emoji>"
E_FLASH = "<emoji id='5345905193005371012'>⚡️</emoji>"
E_LOCK  = "<emoji id='6115973347206501819'>🔒</emoji>"

# ==========================================
# 🛡️ ᴏᴡɴᴇʀ ᴄʜᴇᴄᴋᴇʀ ꜰᴜɴᴄᴛɪᴏɴ (STRICT SECURITY)
# ==========================================
def is_owner(user_id):
    return user_id == OWNER_ID

# ==========================================
# ☢️ 1. SET BOT NAME (/setbotname) - DIRECT HTTP API 🔥
# ==========================================
@Client.on_message(filters.command("setbotname"))
async def set_bot_name(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not is_owner(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʏ ᴇ ʜ  ᴘ ᴏ ᴡ ᴇ ʀ  ꜱ ɪ ʀ ꜰ  ᴏ ᴡ ɴ ᴇ ʀ  ᴋ ᴇ  ᴘ ᴀ ᴀ ꜱ  ʜ ᴀ ɪ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/setbotname [New Name]</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    new_name = message.text.split(None, 1)[1]
    msg = await message.reply_text(f"<blockquote>{E_FLASH} <b>ᴜ ᴘ ᴅ ᴀ ᴛ ɪ ɴ ɢ  ɴ ᴀ ᴍ ᴇ...</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        token = client.bot_token
        if not token:
            return await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ : ʙ ᴏ ᴛ  ᴛ ᴏ ᴋ ᴇ ɴ  ɴ ᴀ ʜ ɪ ɴ  ᴍ ɪ ʟ ᴀ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)

        # 🔥 Direct Request to Telegram Core Servers (No Pyrogram method used)
        encoded_name = urllib.parse.quote(new_name)
        url = f"https://api.telegram.org/bot{token}/setMyName?name={encoded_name}"
        
        request = urllib.request.urlopen(url)
        response = json.loads(request.read().decode('utf-8'))
        
        if response.get("ok"):
            await msg.edit_text(f"<blockquote>{E_CHECK} <b>ɴ ᴀ ᴀ ᴍ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
        else:
            error_desc = response.get('description', 'Unknown Error')
            await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴀ ᴘ ɪ  ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{error_desc}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{e}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 2. SET BOT BIO (/setbotbio) - DIRECT HTTP API 🔥
# ==========================================
@Client.on_message(filters.command("setbotbio"))
async def set_bot_bio(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not is_owner(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʏ ᴇ ʜ  ᴘ ᴏ ᴡ ᴇ ʀ  ꜱ ɪ ʀ ꜰ  ᴏ ᴡ ɴ ᴇ ʀ  ᴋ ᴇ  ᴘ ᴀ ᴀ ꜱ  ʜ ᴀ ɪ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/setbotbio [New Bio]</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    new_bio = message.text.split(None, 1)[1]
    
    if len(new_bio) > 120:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ʙ ɪ ᴏ  ʟ ɪ ᴍ ɪ ᴛ :</b> ꜱ ɪ ʀ ꜰ  120  ᴄ ʜ ᴀ ʀ ᴀ ᴄ ᴛ ᴇ ʀ ꜱ  ᴀ ʟ ʟ ᴏ ᴡ ᴇ ᴅ  ʜ ᴀ ɪ ɴ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    msg = await message.reply_text(f"<blockquote>{E_FLASH} <b>ᴜ ᴘ ᴅ ᴀ ᴛ ɪ ɴ ɢ  ʙ ɪ ᴏ...</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        token = client.bot_token
        if not token:
            return await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ : ʙ ᴏ ᴛ  ᴛ ᴏ ᴋ ᴇ ɴ  ɴ ᴀ ʜ ɪ ɴ  ᴍ ɪ ʟ ᴀ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)

        # 🔥 Direct Request to Telegram Core Servers (No Pyrogram method used)
        encoded_bio = urllib.parse.quote(new_bio)
        url = f"https://api.telegram.org/bot{token}/setMyShortDescription?short_description={encoded_bio}"
        
        request = urllib.request.urlopen(url)
        response = json.loads(request.read().decode('utf-8'))
        
        if response.get("ok"):
            await msg.edit_text(f"<blockquote>{E_CHECK} <b>ʙ ɪ ᴏ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
        else:
            error_desc = response.get('description', 'Unknown Error')
            await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴀ ᴘ ɪ  ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{error_desc}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{e}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 3. SET BOT PFP (/setbotpfp) - WORKING METHOD ✅
# ==========================================
@Client.on_message(filters.command("setbotpfp"))
async def set_bot_pfp(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not is_owner(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʏ ᴇ ʜ  ᴘ ᴏ ᴡ ᴇ ʀ  ꜱ ɪ ʀ ꜰ  ᴏ ᴡ ɴ ᴇ ʀ  ᴋ ᴇ  ᴘ ᴀ ᴀ ꜱ  ʜ ᴀ ɪ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> ᴋ ɪ ꜱ ɪ  ᴘ ʜ ᴏ ᴛ ᴏ  ᴘ ᴇ  ʀ ᴇ ᴘ ʟ ʏ  ᴋ ᴀ ʀ ᴋ ᴇ  <code>/setbotpfp</code>  ʟ ɪ ᴋ ʜ ᴏ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    msg = await message.reply_text(f"<blockquote>{E_FLASH} <b>ᴅ ᴏ ᴡ ɴ ʟ ᴏ ᴀ ᴅ ɪ ɴ ɢ  ᴘ ʜ ᴏ ᴛ ᴏ...</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        # Download image to server
        photo_path = await message.reply_to_message.download()
        await msg.edit_text(f"<blockquote>{E_FLASH} <b>ᴜ ᴘ ʟ ᴏ ᴀ ᴅ ɪ ɴ ɢ  ɴ ᴇ ᴡ  ᴘ ꜰ ᴘ...</b></blockquote>", parse_mode=enums.ParseMode.HTML)
        
        await client.set_profile_photo(photo=photo_path)
        
        # Cleanup
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        await msg.edit_text(f"<blockquote>{E_CHECK} <b>ᴘ ʀ ᴏ ꜰ ɪ ʟ ᴇ  ᴘ ɪ ᴄ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
        
    except FloodWait as fw:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ꜰ ʟ ᴏ ᴏ ᴅ ᴡ ᴀ ɪ ᴛ :</b> {fw.value} ꜱ ᴇ ᴄ ᴏ ɴ ᴅ ꜱ  ᴡ ᴀ ɪ ᴛ  ᴋ ᴀ ʀ ᴏ !</blockquote>", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{e}</code></blockquote>", parse_mode=enums.ParseMode.HTML)
