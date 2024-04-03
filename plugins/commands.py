import logging
from pyrogram import Client, filters
from info import *
from Script import script
from database.database import db
from utils import *

logger = logging.getLogger(__name__)

@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            LOG_CHANNEL,
               f"#NewUser\n\nUser ID: {message.from_user.id}\nUsername: {message.from_user.username}"
        )
    
    if AUTH_CHANNEL:
        fsub = await handle_force_subscribe(client, message)
        if fsub == 400:
            return
    
    await message.reply_text(
        text=script.START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=script.START_BUTTONS
    )
    
    if data := message.text.split("-", 1)[0] == "verify":
        userid = message.text.split("-", 2)[1]
        token = message.text.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid or expired link!</b>",
            )
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await message.reply_text(
                text=f"<b>Hey User, You are successfully verified! Now you have unlimited access for all movies till the next verification, which is after 6 hours from now.</b>",
            )
            await verify_user(client, userid, token)
            return
        else:
            return await message.reply_text(
                text="<b>Invalid or expired link!</b>",
            )

@Client.on_message(filters.command('logs') & filters.user(OWNER_ID))
async def log_file(client, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
