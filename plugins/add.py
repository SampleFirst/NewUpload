from pyrogram import Client, filters
from info import PREMIUM_CHAT, LOG_CHANNEL

# Function to forward messages containing specific text
@Client.on_message(filters.chat(LOG_CHANNEL) & filters.text)
async def forward_message(client, message):
    if "/add" in message.text:  # Replace "specific_text" with the text you want to search for
        await client.forward_messages(PREMIUM_CHAT, message.chat.id, message.message_id)
        
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

