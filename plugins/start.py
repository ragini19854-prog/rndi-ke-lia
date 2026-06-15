import time
import psutil
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import MessageNotModified
from core import database
from config import OWNER_ID, SUDO_USERS, LOGGER

# ==========================================
# ⚙️ SYSTEM CORE VARS
# ==========================================
BOOT_TIME = time.time()

def get_readable_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d > 0: return f"{d}ᴅ {h}ʜ"
    return f"{h}ʜ {m}ᴍ"

def make_bar(percent):
    filled = int(percent / 10)
    empty = 10 - filled
    return f"[{'▰' * filled}{'▱' * empty}]"

# ==========================================
# 🎨 DYNAMIC UI GENERATOR
# ==========================================
def generate_start_panel(user_name: str, user_id: int, ping_time: float) -> str:
    """Generates the advanced HTML blockquote start panel."""
    uptime = get_readable_time(int(time.time() - BOOT_TIME))
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram_usage = psutil.virtual_memory().percent
    cpu_bar = make_bar(cpu_usage)
    ram_bar = make_bar(ram_usage)
    
    return f"""<blockquote><emoji id="5039816072253932764">💎</emoji> <b>ᴍᴀᴅᴀʀᴀ ꜱᴩᴀᴍ ʙᴏᴛ</b> <emoji id="5039816072253932764">💎</emoji>
━━━━━━━━━━━━━━━━━━
╭── <emoji id="6118612596019958861">👑</emoji> <b>ᴜꜱᴇʀ ɪɴꜰᴏ</b>
│   ├── ᴍᴀꜱᴛᴇʀ: <code>{user_name}</code>
│   ╰── ᴜɪᴅ: <code>{user_id}</code>
│
├── <emoji id="5199785165735367039">⚡️</emoji> <b>ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ</b>
│   ├── ʟᴀᴛᴇɴᴄʏ: <code>{round(ping_start, 2)} ᴍꜱ</code>
│   ╰── ᴜᴩᴛɪᴍᴇ: <code>{uptime}</code>
│
╰── 📊 <b>ʜᴀʀᴅᴡᴀʀᴇ ʟᴏᴀᴅ</b>
    ├── ᴄᴩᴜ: {cpu_bar} <code>{cpu_usage}%</code>
    ╰── ʀᴀᴍ: {ram_bar} <code>{ram_usage}%</code>
━━━━━━━━━━━━━━━━━━
<emoji id="5042209657527993345">💀</emoji> [ ᴍᴀᴅᴀʀᴀ ꜱᴩᴀᴍ ʙᴏᴛ : ᴏɴʟɪɴᴇ ]</blockquote>"""

# 🎛️ Default Keyboard with Refresh Button
def get_start_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url="https://t.me/Egoist_Destroyer"),
            InlineKeyboardButton("💀 ᴍᴜꜱɪᴄ ʙᴏᴛ", url="http://t.me/HINATA_MUSIC_PLAYER_BOT")
        ],
        [
            InlineKeyboardButton("🔥 ᴄʜᴀɴɴᴇʟ", url="https://t.me/EDITING_PFP"),
            InlineKeyboardButton("💬 ɢʀᴏᴜᴩ", url="https://t.me/+w5QsmWX0sPg3Yzk1")
        ],
        [
            InlineKeyboardButton("🔄 ʀᴇꜰʀᴇꜱʜ ꜱᴛᴀᴛꜱ", callback_data="refresh_stats")
        ]
    ])

# ==========================================
# 🚀 COMMAND: /start
# ==========================================
@Client.on_message(filters.command("start") & filters.private)
async def matrix_start(client, message):
    start_t = time.time()
    me = await client.get_me()
    
    user_name = message.from_user.first_name if message.from_user else "ɢᴜᴇꜱᴛ"
    user_id = message.from_user.id if message.from_user else 0
    
    # 🗃️ DB Hook: Naya user aate hi chupke se save kar lo
    if user_id:
        try:
            await database.add_user(user_id)
        except Exception as e:
            LOGGER.error(f"DB User Hook Error: {e}")

    global ping_start
    ping_start = (time.time() - start_t) * 1000
    
    start_text = generate_start_panel(user_name, user_id, ping_start)
    keyboard = get_start_keyboard()

    media_data = await database.get_start_media(me.id)
    
    if media_data:
        file_id = media_data["file_id"]
        m_type = media_data["media_type"]
        
        try:
            if m_type == "photo":
                await message.reply_photo(file_id, caption=start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
            elif m_type == "video":
                await message.reply_video(file_id, caption=start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
            elif m_type == "animation":
                await message.reply_animation(file_id, caption=start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
            elif m_type == "sticker":
                await message.reply_sticker(file_id)
                await message.reply_text(start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        except Exception:
            await message.reply_text(start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text(start_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)

# ==========================================
# 🔄 CALLBACK: Refresh Stats
# ==========================================
@Client.on_callback_query(filters.regex("^refresh_stats$"))
async def refresh_start_stats(client, callback_query: CallbackQuery):
    start_t = time.time()
    
    user_name = callback_query.from_user.first_name
    user_id = callback_query.from_user.id
    ping_time = (time.time() - start_t) * 1000
    
    new_text = generate_start_panel(user_name, user_id, ping_time)
    keyboard = get_start_keyboard()
    
    try:
        if callback_query.message.media:
            await callback_query.message.edit_caption(caption=new_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        else:
            await callback_query.message.edit_text(text=new_text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)
        await callback_query.answer("⚡ Stats Updated Successfully!", show_alert=False)
    except MessageNotModified:
        await callback_query.answer("⚠️ Stats are already up to date!", show_alert=False)
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)

# ==========================================
# ⚙️ COMMAND: /setstart (Sudo Only)
# ==========================================
def is_sudo(_, __, message):
    return message.from_user and message.from_user.id in SUDO_USERS

sudo_filter = filters.create(is_sudo)

@Client.on_message(filters.command("setbotstart") & sudo_filter)
async def set_start_media_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ <b>ᴇʀʀᴏʀ:</b> <code>ᴋɪꜱɪ ᴩʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ɢɪꜰ ʏᴀ ꜱᴛɪᴄᴋᴇʀ ᴩᴇ ʀᴇᴩʟʏ ᴋᴀʀᴋᴇ /setbotstart ʟɪᴋʜᴏ!</code>", parse_mode=enums.ParseMode.HTML)

    reply = message.reply_to_message
    file_id, media_type = None, None

    if reply.photo: file_id, media_type = reply.photo.file_id, "photo"
    elif reply.video: file_id, media_type = reply.video.file_id, "video"
    elif reply.animation: file_id, media_type = reply.animation.file_id, "animation"
    elif reply.sticker: file_id, media_type = reply.sticker.file_id, "sticker"
    else:
        return await message.reply_text("❌ <b>ɪɴᴠᴀʟɪᴅ ᴍᴇᴅɪᴀ:</b> <code>ꜱɪʀꜰ ᴩʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ɢɪꜰ ʏᴀ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ ᴋᴀʀ ꜱᴀᴋᴛᴇ ʜᴏ.</code>", parse_mode=enums.ParseMode.HTML)

    me = await client.get_me()
    await database.set_start_media(me.id, file_id, media_type)
    
    LOGGER.info(f"🖼️ User {message.from_user.id} updated Start Media for Node: {me.first_name}")
    await message.reply_text(f"✅ <b>ᴍᴀᴅᴀʀᴀ ᴍᴇᴅɪᴀ ꜱᴇᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜰᴏʀ</b> <code>{me.first_name}</code>!\n<code>ᴀʙ /start ᴋᴀʀᴋᴇ ᴄʜᴇᴄᴋ ᴋᴀʀ ʟᴏ.</code>", parse_mode=enums.ParseMode.HTML)
