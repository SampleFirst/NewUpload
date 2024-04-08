from pyrogram import Client, filters
from info import ADMINS 


@Client.on_message(filters.private & filters.command("send"))
async def send_to_admin(bot, message):
    if message.reply_to_message:
        if message.from_user.id not in ADMINS:
            await message.reply_to_message.forward(chat_id=ADMINS[0])
            await message.reply_text("<b>Your message has been successfully sent to Admin.</b>")
            return
        else:
            await message.reply_text("<b>You're an admin. You can't use this command.</b>")
    else:
        await message.reply_text("<b>Reply to a message with /send to forward it to an admin.</b>")

@Client.on_message(filters.private & ~filters.command("send") & filters.reply)
async def forward_reply_to_user(bot, message):
    if message.reply_to_message.forward_from.id in ADMINS:
        await message.reply_to_message.forward(chat_id=message.from_user.id)
