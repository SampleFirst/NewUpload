from pyrogram import Client, filters 
from info import *

@Client.on_message(filters.command("send"))
async def send_msg(bot, message):
    if message.reply_to_message:
        if message.from_user.id not in ADMINS:
            await message.reply_to_message.forward(chat_id=ADMINS[0])
            await message.reply_text("<b>Your message has been successfully sent to Admin.</b>")
            return
        else:
            await message.reply_text("<b>Use this command as a reply to any message to contact an admin. For example: /send</b>")
    else:
        target_id = message.text.split(" ", 1)[1]
        out = "Users Saved In DB Are:\n\n"
        success = False
        try:
            user = await bot.get_users(int(target_id))
            users = await db.get_all_users()  # Assuming you have a db object
            async for usr in users:
                out += f"{usr['id']}\n"
            if str(user.id) in out:
                await message.copy(chat_id=user.id)
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Your message has been successfully sent to {user.mention}.</b>")
            else:
                await message.reply_text("<b>This user hasn't started this bot yet!</b>")
        except Exception as e:
            await message.reply_text(f"<b>Error: {e}</b>")

