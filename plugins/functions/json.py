import os
import json
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command(["json", "js"]))
async def jsonify(client, message):
    url = None

    if message.reply_to_message and message.reply_to_message.text:
        url = message.reply_to_message.text
    elif len(message.command) > 1:
        url = message.command[1]

    if url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    filename = "json_file.json"
                    with open(filename, "w") as json_file:
                        json.dump(data, json_file, indent=4)
                    await message.reply_document(
                        document=filename,
                        caption="Here's the JSON file for the provided URL.",
                        disable_notification=True,
                        quote=True
                    )
                    os.remove(filename)
        except Exception as e:
            await message.reply_text(
                f"An error occurred while fetching or processing the JSON data: {e}",
                reply_markup=reply_markup,
                quote=True
            )
    else:
        await message.reply_text(
            "Please provide a valid URL to fetch JSON data from.",
            reply_markup=reply_markup,
            quote=True
        )
