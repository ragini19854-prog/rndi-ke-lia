import time
from pyrogram import Client, filters, enums
from core import database
from config import OWNER_ID

# ==========================================
# 👑 SECURITY: SUDO + OWNER ASYNC FILTER
# ==========================================
async def is_sudo_or_owner(_, client, message):
    if not message.from_user:
        return False
    # Agar message bhejne wala Owner hai, to turant True!
    if message.from_user.id == OWNER_ID:
        return True
    # Varna database me check karo ki kya wo Sudo hai?
    return await database.is_sudo_db(message.from_user.id)

# Filter create kiya gaya
sudo_filter = filters.create(is_sudo_or_owner)

# ==========================================
# ⚡ COMMAND: /ping (GC without Admin works!)
# ==========================================
@Client.on_message(filters.command("ping") & sudo_filter)
async def matrix_ping(client, message):
    # Time calculate start
    start_time = time.time()
    
    # User info
    user_name = message.from_user.first_name if message.from_user else "ʜᴀᴄᴋᴇʀ"
    
    # Pehle ek dummy message bhejenge time check karne ke liye (Sigma style in Small Caps)
    reply_msg = await message.reply_text("<blockquote><emoji id=\"5199785165735367039\">⚡️</emoji> <code>ᴀᴜᴋᴀᴀᴛ ɴᴀᴀᴩ ʀᴀʜᴀ ʜᴜɴ...</code></blockquote>", parse_mode=enums.ParseMode.HTML)
    
    # Time calculate end
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 2)
    
    # Premium Aesthetic Blockquote with Sigma/Toxic Vibes (Small Caps)
    ping_text = f"""<blockquote><emoji id="5199785165735367039">⚡️</emoji> <b>ᴩᴏɴɢ - ʙᴀᴀᴩ ᴀᴀʏᴀ</b> ❞
━━━━━━━━━━━━━━━━━━
<emoji id="5039816072253932764">💎</emoji> ʟᴀᴛᴇɴᴄʏ : <code>{ping_time} ᴍꜱ</code>
<emoji id="5041792560368977040">👑</emoji> ʀᴇQᴜᴇꜱᴛᴇᴅ ʙʏ : <code>{user_name}</code>
━━━━━━━━━━━━━━━━━━
<emoji id="5260750418320836046">🚨</emoji> <b>ʜᴀᴛᴇʀꜱ ᴋɪ ᴍᴋᴄ</b> 🖕
<emoji id="5042209657527993345">💀</emoji> [ ꜱʏꜱᴛᴇᴍ ꜰᴀᴀᴅ ᴅɪʏᴀ ]</blockquote>"""
    
    # Message ko edit kar ke final look denge
    await reply_msg.edit_text(ping_text, parse_mode=enums.ParseMode.HTML)
