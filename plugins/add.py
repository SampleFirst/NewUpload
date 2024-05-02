from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import verify_user
from info import ADMINS


@Client.on_message(filters.command("addpre") & filters.user(ADMINS))
async def addpre(client, message):
    if len(message.command) != 2:
        await message.reply_text("Invalid command format. Please use /addpre {userid}-{token}")
        return
    
    try:
        user_token = message.command[1].split('-')
        userid = int(user_token[0])
        token = user_token[1]
        
        await verify_user(client, userid, token)
        await client.send_message(
            userid,
            "For User: You are successfully verified for the next 24 hours.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Click here", url="https://t.me/BraveUpdates/6")]])
        )
        await message.reply(f"{userid} successfully verified for the next 24 hours for all 4 bots.\n\nFor user: Your verification is successful for the next 24 hours for all my bots!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
