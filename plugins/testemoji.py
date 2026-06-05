from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# 🧪 LIVE EMOJI TEST PLUGIN (/testemoji)
# ==========================================

@Client.on_message(filters.command("testemoji"))
async def emoji_test_plugin(client, message):
    
    # 💡 Premium jaisa dikhne wale Normal Unicode Emojis (No IDs used)
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="👑 ᴍʏ ᴍᴀꜱᴛᴇʀ", callback_data="test_master"),
                InlineKeyboardButton(text="🦚 ɴᴇᴛᴡᴏʀᴋ", callback_data="test_network")
            ],
            [
                InlineKeyboardButton(text="🌸 ᴍʏ ʜᴏᴍᴇ", callback_data="test_home"),
                InlineKeyboardButton(text="🎵 ᴜᴘᴘᴇʀᴍᴏᴏɴ ᴛᴜɴᴇꜱ", callback_data="test_tunes")
            ]
        ]
    )

    # 🌳 Tree Style + Small Caps text (No HTML tags, purely raw text)
    text = (
        "╭━━ [ ᴇᴍᴏᴊɪ ʀᴇᴀʟɪᴛʏ ᴄʜᴇᴄᴋ ☠️ ] ━━\n"
        "├ ⇛ ʙᴏꜱꜱ, ɴɪᴄʜᴇ ʙᴜᴛᴛᴏɴꜱ ᴄʜᴇᴄᴋ ᴋᴀʀ ᴀʙʜɪ!\n"
        "╰ ⇛ ᴀɢᴀʀ ʏᴇ ᴠɪᴅᴇᴏ ᴊᴀɪꜱᴇ ᴅɪᴋʜ ʀᴀʜᴇ ʜᴀɪɴ, ᴛᴏ ᴍᴀᴛʟᴀʙ ᴡᴏ ɴᴏʀᴍᴀʟ ᴇᴍᴏᴊɪ ʜɪ ᴛʜᴇ! ⚡"
    )

    # Sending the message with buttons
    await message.reply_text(text, reply_markup=buttons)

# ==========================================
# ⚠️ DUMMY CALLBACK HANDLER (Taki button dabane pe error na aaye)
# ==========================================

@Client.on_callback_query(filters.regex(r"^test_"))
async def test_callback(client, callback_query):
    await callback_query.answer("☠️ ᴍᴏɴꜱᴛᴇʀ ᴇᴍᴏᴊɪ ᴛᴇꜱᴛ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ! 🔥", show_alert=True)
