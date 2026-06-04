import os
import re
import math
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
# 🛡️ ꜱᴜᴅᴏ & ᴏᴡɴᴇʀ ᴄʜᴇᴄᴋᴇʀ ꜰᴜɴᴄᴛɪᴏɴ 
# ==========================================
async def check_sudo(user_id):
    if user_id == OWNER_ID:
        return True
    return await database.is_sudo_db(user_id)

# ==========================================
# 📡 THE LIVE SCANNER ENGINE (Auto-Detects Commands)
# ==========================================
def get_all_commands():
    commands = set()
    # 📂 Pura directory scan karega (Venv aur hidden files chhod ke)
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('venv', 'env', '__pycache__')]
        for file in files:
            if file.endswith(".py"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        # 🧠 RegEx se saare filters.command nikalega
                        matches = re.findall(r'filters\.command\(\s*(?:\[([^\]]+)\]|([\'"][^\'"]+[\'"]))\s*\)', content)
                        for match in matches:
                            raw_cmds = match[0] if match[0] else match[1]
                            extracted = re.findall(r'[\'"]([^\'"]+)[\'"]', raw_cmds)
                            for cmd in extracted:
                                commands.add(cmd.lower())
                except Exception:
                    pass
    return sorted(list(commands))

# ==========================================
# 📑 PAGINATION BUILDER 
# ==========================================
def build_help_page(page_num, user_id):
    cmds = get_all_commands()
    items_per_page = 12
    total_pages = math.ceil(len(cmds) / items_per_page)
    
    if total_pages == 0:
        total_pages = 1

    # Page Limits
    if page_num < 1: page_num = 1
    if page_num > total_pages: page_num = total_pages

    start_idx = (page_num - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_cmds = cmds[start_idx:end_idx]

    # 🎨 FORMATTING TEXT IN SMALL CAPS & HTML
    text = f"<blockquote>{E_CROWN} <b>ᴛ ʜ ᴇ  ᴀ ɴ ᴜ  ᴍ ᴀ ᴛ ʀ ɪ x  ᴄ ᴏ ᴍ ᴍ ᴀ ɴ ᴅ ꜱ</b> {E_CROWN}\n"
    text += f"━━━━━━━━━━━━━━━━━━\n"
    for cmd in page_cmds:
        text += f"{E_FLASH} <code>/{cmd}</code>\n"
    text += f"━━━━━━━━━━━━━━━━━━\n"
    text += f"<b>[ ᴘ ᴀ ɢ ᴇ : {page_num} / {total_pages} ]</b></blockquote>"

    # 🎛️ BUTTONS LOGIC
    buttons = []
    nav_row = []
    
    if page_num > 1:
        nav_row.append(InlineKeyboardButton("⏪ ʙ ᴀ ᴄ ᴋ", callback_data=f"help_prev_{page_num-1}_{user_id}"))
    
    if page_num < total_pages:
        nav_row.append(InlineKeyboardButton("ɴ ᴇ x ᴛ ⏩", callback_data=f"help_next_{page_num+1}_{user_id}"))
        
    if nav_row:
        buttons.append(nav_row)
        
    buttons.append([InlineKeyboardButton("❌ ᴄ ʟ ᴏ ꜱ ᴇ", callback_data=f"help_close_{user_id}")])

    return text, InlineKeyboardMarkup(buttons)

# ==========================================
# ☢️ HELP COMMAND (/help)
# ==========================================
@Client.on_message(filters.command(["help", "alive"]))
async def live_help_command(client, message):
    user_id = message.from_user.id if message.from_user else 0
    
    # 🛑 Sudo Check
    if not await check_sudo(user_id):
        return await message.reply_text(f"<blockquote>{E_DEVIL} <b>ᴀ ᴜ ᴋ ᴀ ᴀ ᴛ  ᴍ ᴇɪ ɴ  ʀ ᴇ ʜ  ʟ ᴏ ᴅ ᴇ ,  ʏ ᴇ ʜ  ꜱ ɪ ʀ ꜰ  ꜱ ᴜ ᴅ ᴏ  ᴋ ᴇ  ʟ ɪ ʏ ᴇ  ʜ ᴀ ɪ ! 🖕</b></blockquote>", parse_mode=enums.ParseMode.HTML)

    text, reply_markup = build_help_page(1, user_id)
    await message.reply_text(text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)

# ==========================================
# 🖲️ CALLBACK QUERY HANDLER (Buttons)
# ==========================================
@Client.on_callback_query(filters.regex(r"^help_(prev|next|close)_(\d+)_(\d+)$") | filters.regex(r"^help_close_(\d+)$"))
async def help_pagination_callback(client, callback_query: CallbackQuery):
    clicker_id = callback_query.from_user.id
    data = callback_query.data.split("_")
    
    # Extract Original User ID from callback data
    original_user_id = int(data[-1])

    # 🛑 Authorization: Jisne command diya, sirf wahi button daba sakta hai
    if clicker_id != original_user_id:
        return await callback_query.answer("🖕 ᴀ ᴘ ɴ ᴇ  ᴄ ᴏ ᴍ ᴍ ᴀ ɴ ᴅ  ᴘ ᴇ  ᴄ ʟ ɪ ᴄ ᴋ  ᴋ ᴀ ʀ ɴ ᴀ  ʟ ᴏ ᴅ ᴇ !", show_alert=True)

    action = data[1]

    if action == "close":
        await callback_query.message.delete()
        return await callback_query.answer("ꜱ ʏ ꜱ ᴛ ᴇ ᴍ  ᴄ ʟ ᴏ ꜱ ᴇ ᴅ ! 💥", show_alert=False)

    page_num = int(data[2])
    text, reply_markup = build_help_page(page_num, original_user_id)
    
    try:
        await callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
    except Exception:
        pass # Ignore message not modified errors
    
    await callback_query.answer()
