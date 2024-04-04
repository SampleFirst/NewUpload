from pyrogram import Client, filters
from utils import premium_user, remove_premium_user
from info import ADMINS 

# Command to update user's premium status
@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        await premium_user(client, user_id)
        await message.reply_text("User's premium status updated successfully!")
    elif len(message.command) > 1:  # Check if command has additional parameters
        user_id = int(message.command[1])
        await premium_user(client, user_id)
        await message.reply_text("User's premium status updated successfully!")
    else:
        await message.reply_text("Please reply to the user or specify the user ID whose premium status you want to update.")

# Command to update user's premium status
@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        await remove_premium_user(client, user_id)
        await message.reply_text("User's premium status remove successfully!")
    elif len(message.command) > 1:  # Check if command has additional parameters
        user_id = int(message.command[1])
        await premium_user(client, user_id)
        await message.reply_text("User's premium status remove successfully!")
    else:
        await message.reply_text("Please reply to the user or specify the user ID whose premium status you want to remove.")
