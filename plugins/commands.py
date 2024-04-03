import logging
from pyrogram import Client, filters
from plugins.config import Config
from plugins.script import Translation
from plugins.database.database import db
from plugins.functions.forcesub import handle_force_subscribe

logger = logging.getLogger(__name__)

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you sar :(")
    
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
        await bot.send_message(
            Config.LOG_CHANNEL,
               f"#NewUser\n\nUser ID: {update.from_user.id}\nUsername: {update.from_user.username}"
        )
    
    if Config.UPDATES_CHANNEL:
        fsub = await handle_force_subscribe(bot, update)
        if fsub == 400:
            return
    
    await update.reply_text(
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Translation.START_BUTTONS
    )
    
    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
            )
        is_valid = await check_token(bot, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>Hᴇʏ User, Yᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\nNᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴍᴏᴠɪᴇs ᴛɪʟʟ ᴛʜᴇ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴡʜɪᴄʜ ɪs ᴀғᴛᴇʀ 6 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ.</b>",
            )
            await verify_user(bot, userid, token)
            return
        else:
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
            )

@Client.on_message(filters.command('logs') & filters.user(Config.OWNER_ID))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
