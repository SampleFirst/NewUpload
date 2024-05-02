from pyrogram import Client, filters
from info import PREMIUM_CHAT

# Define your function to handle messages
@Client.on_message(filters.chat("PREMIUM_CHAT") & filters.text & filters.regex(r'^/add24 \d+ \| \w+'))
async def add(client, message):
    # Extract user ID and token from the message
    user_id, token = message.text.split()[1].split("|")
    user_id = int(user_id.strip())
    token = token.strip()
    
    # Reply to the message
    await message.reply_text(f"User ID: {user_id}, Token: {token}")
    
    # Send a message to the user with the provided user ID
    await client.send_message(user_id, "Your message here")

