from pyrogram import Client, filters
from pyrogram.types import MessageEntity
from typing import Union

# Assume ADMINS and extract_user function are imported properly

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
    status_message = await message.reply_text("`Fetching user info...`")
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await bot.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("No valid user_id / message specified")
    await message.reply_to_message.forward(chat_id=from_user_id)
    await status_message.edit(f"<b>Your message has been successfully sent to {from_user.first_name}.</b>")
    return

def extract_user(message: Message) -> Union[int, str]:
    user_id = None
    user_first_name = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name
    elif len(message.text) > 1:
        if len(message.entities) > 1 and message.entities[1].type == MessageEntity.TEXT_MENTION:
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.text[1]
            user_first_name = user_id
        try:
            user_id = int(user_id)
        except ValueError:
            pass
    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
    return user_id, user_first_name
