import os
import asyncio
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
# ☢️ 1. SET BOT NAME (/setbotname) - Bot API Supported ✅
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
        # 🔥 Uses Official Bot API Method
        await client.set_bot_name(name=new_name)
        await msg.edit_text(f"<blockquote>{E_CHECK} <b>ɴ ᴀ ᴀ ᴍ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{e}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 2. SET BOT BIO (/setbotbio) - Bot API Supported ✅
# ==========================================
@Client.on_message(filters.command("setbotbio"))
async def set_bot_bio(client, message):
    user_id = message.from_user.id if message.from_user else 0
    if not is_owner(user_id):
        return await message.reply_text(f"<blockquote>{E_LOCK} <b>ʏ ᴇ ʜ  ᴘ ᴏ ᴡ ᴇ ʀ  ꜱ ɪ ʀ ꜰ  ᴏ ᴡ ɴ ᴇ ʀ  ᴋ ᴇ  ᴘ ᴀ ᴀ ꜱ  ʜ ᴀ ɪ  ʟ ᴏ ᴅ ᴇ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    if len(message.command) < 2:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ᴜ ꜱ ᴀ ɢ ᴇ :</b> <code>/setbotbio [New Bio]</code></blockquote>", parse_mode=enums.ParseMode.HTML)

    new_bio = message.text.split(None, 1)[1]
    
    # ⚠️ Bot API Short Description Limit is 120 Characters
    if len(new_bio) > 120:
        return await message.reply_text(f"<blockquote>{E_WARN} <b>ʙ ɪ ᴏ  ʟ ɪ ᴍ ɪ ᴛ :</b> ꜱ ɪ ʀ ꜰ  120  ᴄ ʜ ᴀ ʀ ᴀ ᴄ ᴛ ᴇ ʀ ꜱ  ᴀ ʟ ʟ ᴏ ᴡ ᴇ ᴅ  ʜ ᴀ ɪ ɴ !</blockquote>", parse_mode=enums.ParseMode.HTML)

    msg = await message.reply_text(f"<blockquote>{E_FLASH} <b>ᴜ ᴘ ᴅ ᴀ ᴛ ɪ ɴ ɢ  ʙ ɪ ᴏ...</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    try:
        # 🔥 Uses Official Bot API Method for "About" section
        await client.set_bot_short_description(short_description=new_bio)
        await msg.edit_text(f"<blockquote>{E_CHECK} <b>ʙ ɪ ᴏ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"<blockquote>{E_DEVIL} <b>ᴇ ʀ ʀ ᴏ ʀ :</b> <code>{e}</code></blockquote>", parse_mode=enums.ParseMode.HTML)

# ==========================================
# ☢️ 3. SET BOT PFP (/setbotpfp) - Strictly BotFather / Userbot
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
        
        # Userbot Method (Will fail on pure Bot Token)
        await client.set_profile_photo(photo=photo_path)
        
        if os.path.exists(photo_path):
            os.remove(photo_path)
            
        await msg.edit_text(f"<blockquote>{E_CHECK} <b>ᴘ ʀ ᴏ ꜰ ɪ ʟ ᴇ  ᴘ ɪ ᴄ  ᴜ ᴘ ᴅ ᴀ ᴛ ᴇ ᴅ  ꜱ ᴜ ᴄ ᴄ ᴇ ꜱ ꜱ ꜰ ᴜ ʟ ʟ ʏ !</b></blockquote>", parse_mode=enums.ParseMode.HTML)
        
    except Exception:
        # 🔥 Catching the token limitation smartly
        await msg.edit_text(f"<blockquote>{E_WARN} <b>ᴛ ᴇ ʟ ᴇ ɢ ʀ ᴀ ᴍ  ꜱ ᴇ ᴄ ᴜ ʀ ɪ ᴛ ʏ :</b> ʙ ᴏ ᴛ  ᴛ ᴏ ᴋ ᴇ ɴ  ᴀ ᴘ ɴ ɪ  ᴅ ᴘ  x ᴜ ᴅ  ᴄ ʜ ᴀ ɴ ɢ ᴇ  ɴ ᴀ ʜ ɪ ɴ  ᴋ ᴀ ʀ  ꜱ ᴀ ᴋ ᴛ ᴀ ! ᴘ ꜰ ᴘ  ᴋ ᴇ  ʟ ɪ ʏ ᴇ  @BotFather ᴋ ᴀ  ᴜ ꜱ ᴇ  ᴋ ᴀ ʀ ᴏ .</blockquote>", parse_mode=enums.ParseMode.HTML)
