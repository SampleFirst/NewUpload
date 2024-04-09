from pyrogram import Client
from pyrogram import filters
import requests


# Define the command to trigger the action
@Client.on_message(filters.command("extract")
def extract_media(client, message):
    # Check if the replied message contains a URL
    if message.reply_to_message and message.reply_to_message.text:
        url = message.reply_to_message.text
        # Send a request to the URL to fetch the media data
        response = requests.get(url)
        if response.ok:
            media_data = response.json()
            # Send the media JSON data back to the user
            client.send_message(
                chat_id=message.chat.id,
                text=str(media_data)  # Convert the JSON data to a string
            )
        else:
            client.send_message(
                chat_id=message.chat.id,
                text="Failed to fetch media data from the provided URL."
            )
    else:
        client.send_message(
            chat_id=message.chat.id,
            text="Please reply to a message containing a URL."
        )

