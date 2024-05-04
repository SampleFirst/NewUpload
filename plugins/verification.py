from pyrogram import Client, filters
from database.database import db
from info import ADMINS 

@Client.on_message(filters.command("update_users") & filters.user(ADMINS))
async def update_users(client, message):
    async for user in await db.get_all_users():  # Added await here
        user_id = user.get("id")
        short_temp = "1"
        date_temp = "1999-12-31"
        time_temp = "23:59:59"
        await db.update_verification(user_id, short_temp, date_temp, time_temp)
    
    await message.reply_text("All users updated with default verification status.")
    
