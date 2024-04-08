from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Union
from info import ADMINS 


# Decorator for handling messages that are private and start with /send command
@Client.on_message(filters.private & filters.command("send"))
async def send_to_admin(bot, message):
    # Check if the message is a reply to another message
    if message.reply_to_message:
        # Check if the user is not an admin
        if message.from_user.id not in ADMINS:
            # Forward the replied message to the admin
            await message.reply_to_message.forward(chat_id=ADMINS[0])
            # Reply to the user that their message has been sent to the admin
            await message.reply_text("<b>Your message has been successfully sent to Admin.</b>")
            return
        else:
            # If the user is an admin, reply that they can't use this command
            await message.reply_text("<b>You're an admin. You can't use this command.</b>")
    else:
        # If the message is not a reply, reply with instructions on how to use the command
        await message.reply_text("<b>Reply to a message with /send to forward it to an admin.</b>")

# Decorator for handling messages that are private, a reply, and sent by an admin
@Client.on_message(filters.private & filters.reply & filters.user(ADMINS))
async def forward_reply_to_user(bot, message):
    # Create a status message to show the progress of the command
    status_message = await message.reply_text("`Fetching user info...`")
    # Extract the user ID and first name from the replied message
    from_user = None
    from_user_id, from_user_first_name = extract_user(message)
    try:
        # Try to get the user object using the extracted user ID
        from_user = await bot.get_users(from_user_id)
    except Exception as error:
        # If there's an error, edit the status message with the error message
        await status_message.edit(str(error))
        return
    # If the user object is successfully fetched, continue with the command
    if from_user is not None:
        # Forward the replied message to the user
        await message.reply_to_message.forward(chat_id=from_user_id)
        # Edit the status message with a success message
        await status_message.edit(f"<b>Your message has been successfully sent to {from_user_first_name}.</b>")
        return
    # If the user object is not fetched, edit the status message with an error message
    await status_message.edit("No valid user_id / message specified")
    return

# Define the extract_user function to extract the user ID and first name from the message
def extract_user(message: Message) -> Union[int, str, tuple]:
    user_id = None
    user_first_name = None
    # If the message is a reply, extract the user ID and first name from the replied message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name
    # If the message text starts with a number or a mention, extract the user ID and first name
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
    # If the message is not a reply and the message text does not start with a number or a mention,
    # extract the user ID and first name from the sender
    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name
    # Return the extracted user ID and first name as a tuple
    return user_id, user_first_name

