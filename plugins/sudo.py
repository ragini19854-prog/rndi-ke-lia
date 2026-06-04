from pyrogram import Client, filters, enums
from core import database
from config import OWNER_ID

# ==========================================
# 👑 SECURITY: ONLY OWNER FILTER
# ==========================================
def is_owner(_, __, message):
    return message.from_user and message.from_user.id == OWNER_ID

owner_filter = filters.create(is_owner)

# ==========================================
# 🔍 HELPER: USER EXTRACTOR (Reply, ID, Username)
# ==========================================
async def extract_user(client, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    
    if len(message.command) > 1:
        target = message.text.split(None, 1)[1]
        if target.isdigit():
            target = int(target)
        elif target.startswith("@"):
            target = target.replace("@", "")
        
        try:
            user = await client.get_users(target)
            return user
        except Exception:
            return None
    return None

# ==========================================
# ➕ COMMAND: /addsudobot
# ==========================================
@Client.on_message(filters.command("addsudobot") & owner_filter)
async def add_sudo(client, message):
    user = await extract_user(client, message)
    
    if not user:
        err_txt = f"<blockquote><emoji id=\"6131813839429177098\">🚫</emoji> <b>ᴇʀʀᴏʀ:</b> <code>ᴜꜱᴇʀ ɴᴀʜɪ ᴍɪʟᴀ! ʀᴇᴩʟʏ, ɪᴅ ʏᴀ @ᴜꜱᴇʀɴᴀᴍᴇ ᴅᴏ.</code></blockquote>"
        return await message.reply_text(err_txt, parse_mode=enums.ParseMode.HTML)

    if await database.is_sudo_db(user.id):
        txt = f"<blockquote><emoji id=\"5039665997506675838\">⚠️</emoji> <code>{user.first_name}</code> <b>ᴩᴇʜʟᴇ ꜱᴇ ʜɪ ꜱᴜᴅᴏ ʜᴀɪ!</b></blockquote>"
        return await message.reply_text(txt, parse_mode=enums.ParseMode.HTML)

    await database.add_sudo_db(user.id)
    
    success_txt = f"""<blockquote><emoji id="5041792560368977040">👑</emoji> <b>ꜱᴜᴅᴏ ᴀᴄᴄᴇꜱꜱ ɢʀᴀɴᴛᴇᴅ</b> <emoji id="5041792560368977040">👑</emoji>
━━━━━━━━━━━━━━━━━━
╭── <emoji id="5041784790773138608">👀</emoji> <b>ᴜꜱᴇʀ ɪɴꜰᴏ</b>
│   ├── ɴᴀᴍᴇ: <code>{user.first_name}</code>
│   ╰── ᴜɪᴅ: <code>{user.id}</code>
│
╰── <emoji id="5039793437776282663">✅</emoji> <b>ꜱᴛᴀᴛᴜꜱ:</b> <code>ᴀᴅᴅᴇᴅ ᴛᴏ ᴍᴀᴛʀɪx ꜱᴜᴅᴏ!</code>
━━━━━━━━━━━━━━━━━━
<emoji id="5042209657527993345">💀</emoji> [ ʀᴏᴏᴛ ᴍᴀɪɴꜰʀᴀᴍᴇ : ᴜᴩᴅᴀᴛᴇᴅ ]</blockquote>"""
    
    await message.reply_text(success_txt, parse_mode=enums.ParseMode.HTML)

# ==========================================
# ➖ COMMAND: /delsudobot
# ==========================================
@Client.on_message(filters.command("delsudobot") & owner_filter)
async def del_sudo(client, message):
    user = await extract_user(client, message)
    
    if not user:
        err_txt = f"<blockquote><emoji id=\"6131813839429177098\">🚫</emoji> <b>ᴇʀʀᴏʀ:</b> <code>ᴜꜱᴇʀ ɴᴀʜɪ ᴍɪʟᴀ! ʀᴇᴩʟʏ, ɪᴅ ʏᴀ @ᴜꜱᴇʀɴᴀᴍᴇ ᴅᴏ.</code></blockquote>"
        return await message.reply_text(err_txt, parse_mode=enums.ParseMode.HTML)

    if not await database.is_sudo_db(user.id):
        txt = f"<blockquote><emoji id=\"5039665997506675838\">⚠️</emoji> <code>{user.first_name}</code> <b>ꜱᴜᴅᴏ ʟɪꜱᴛ ᴍᴇ ɴᴀʜɪ ʜᴀɪ!</b></blockquote>"
        return await message.reply_text(txt, parse_mode=enums.ParseMode.HTML)

    await database.del_sudo_db(user.id)
    
    del_txt = f"""<blockquote><emoji id="6199535419168659446">☠</emoji> <b>ꜱᴜᴅᴏ ᴀᴄᴄᴇꜱꜱ ʀᴇᴠᴏᴋᴇᴅ</b> <emoji id="6199535419168659446">☠</emoji>
━━━━━━━━━━━━━━━━━━
╭── <emoji id="5042209657527993345">💀</emoji> <b>ᴜꜱᴇʀ ɪɴꜰᴏ</b>
│   ├── ɴᴀᴍᴇ: <code>{user.first_name}</code>
│   ╰── ᴜɪᴅ: <code>{user.id}</code>
│
╰── <emoji id="6131813839429177098">🚫</emoji> <b>ꜱᴛᴀᴛᴜꜱ:</b> <code>ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴍᴀᴛʀɪx!</code>
━━━━━━━━━━━━━━━━━━
<emoji id="5042209657527993345">💀</emoji> [ ʀᴏᴏᴛ ᴍᴀɪɴꜰʀᴀᴍᴇ : ᴜᴩᴅᴀᴛᴇᴅ ]</blockquote>"""
    
    await message.reply_text(del_txt, parse_mode=enums.ParseMode.HTML)

# ==========================================
# 📋 COMMAND: /sudolistbot
# ==========================================
@Client.on_message(filters.command("sudolistbot") & owner_filter)
async def sudo_list(client, message):
    sudoers = await database.get_all_sudoers()
    
    if not sudoers:
        txt = f"<blockquote><emoji id=\"5039665997506675838\">⚠️</emoji> <b>ᴅᴀᴛᴀʙᴀꜱᴇ ᴍᴇ ᴋᴏɪ ꜱᴜᴅᴏ ᴜꜱᴇʀ ɴᴀʜɪ ʜᴀɪ!</b></blockquote>"
        return await message.reply_text(txt, parse_mode=enums.ParseMode.HTML)

    msg = await message.reply_text("<blockquote><emoji id=\"5199785165735367039\">⚡️</emoji> <code>ꜰᴇᴛᴄʜɪɴɢ ꜱᴜᴅᴏ ɴᴏᴅᴇꜱ...</code></blockquote>", parse_mode=enums.ParseMode.HTML)
    
    list_txt = f"<blockquote><emoji id=\"5039816072253932764\">💎</emoji> <b>ᴍᴀᴛʀɪx ꜱᴜᴅᴏ ɴᴏᴅᴇꜱ</b> <emoji id=\"5039816072253932764\">💎</emoji>\n━━━━━━━━━━━━━━━━━━\n"
    
    count = 1
    for user_id in sudoers:
        try:
            user = await client.get_users(user_id)
            name = user.first_name
        except Exception:
            name = "ᴜɴᴋɴᴏᴡɴ ʜᴀᴄᴋᴇʀ"
            
        list_txt += f" ├ <emoji id=\"5041792560368977040\">👑</emoji> {count}. <code>{name}</code> [<code>{user_id}</code>]\n"
        count += 1
        
    list_txt += f" ╰── <emoji id=\"5039793437776282663\">✅</emoji> <b>ᴛᴏᴛᴀʟ ꜱᴜᴅᴏ:</b> <code>{len(sudoers)}</code>\n━━━━━━━━━━━━━━━━━━\n<emoji id=\"5042209657527993345\">💀</emoji> [ ʀᴏᴏᴛ ᴍᴀɪɴꜰʀᴀᴍᴇ : ᴏɴʟɪɴᴇ ]</blockquote>"
    
    await msg.edit_text(list_txt, parse_mode=enums.ParseMode.HTML)
