from pyrogram import Client, filters
from utils import verify_user
from info import PREMIUM_CHAT

@Client.on_message(filters.command("add24") & filters.channel("PREMIUM_CHAT"))
async def add24(client, message):
    if len(message.command) != 2:
        await message.reply_text("Invalid command format. Please use /add24 {userid} | {token}")
        return
    
    user_info = message.text.split("|")
    userid = user_info[0].split(" ")[1].strip()
    token = user_info[1].strip()
    
    try:
        await verify_user(client, userid, token)
        await client.send_message(
            userid,
            "For User: You are successfully verified for the next 24 hours.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Click here", url="https://t.me/BraveUpdates/6")]])
        )
        await message.reply(f"{userid} successfully verified for the next 24 hours for all 4 bots.\n\nFor user: Your verification is successful for the next 24 hours for all my bots!")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
        
        
