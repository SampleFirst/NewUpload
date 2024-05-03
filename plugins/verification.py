from pyrogram import Client, filters
from database.database import db
from info import ADMINS 

@Client.on_message(filters.command("update_users") & filters.user(ADMINS))
async def update_users(client, message):
    async for user in await db.get_all_users():  # Added await here
        user_id = user.get("id")
        default_verification_status = await db.get_verified(user_id)
        await db.update_verification(user_id, **default_verification_status)
    
    await message.reply_text("All users updated with default verification status.")
