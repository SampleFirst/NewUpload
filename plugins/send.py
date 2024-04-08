from pyrogram import Client, filters
from info import ADMINS 
from utils import extract_user 

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

@Client.on_message(filters.private & filters.reply & filters.user(ADMINS))
async def forward_reply_to_user(bot, message):
    status_message = await message.reply_text(
            "`Fetching user info...`"
        )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("no valid user_id / message specified")
    await message.reply_to_message.forward(chat_id=from_user_id)
    await status_message.edit(f"<b>Your message has been successfully sent to {from_user.first_name}.</b>")
    return
