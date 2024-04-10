import logging
import asyncio
import json
import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Thumbnail
from pyrogram.errors import ChatAdminRequired
from info import *
from Script import script
from utils import *
from plugins.functions.display_progress import humanbytes, TimeFormatter
from plugins.functions.help_uploadbot import DownLoadFile
from plugins.functions.display_progress import progress_for_pyrogram
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from plugins.functions.ran_text import random_char

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command("json") & filters.private & filters.reply)
async def send_json_data(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        # Check if the replied message contains a link
        reply_text = message.reply_to_message.text
        if "http" in reply_text:
            # Extract the link from the replied message
            link = reply_text.split(" ")[0]
            # Process the link to get JSON data
            command_to_exec = ["yt-dlp", "-j", link]
            process = await asyncio.create_subprocess_exec(
                *command_to_exec,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            t_response = stdout.decode().strip()
            if t_response:
                # If JSON data is retrieved, save it to a file
                randem = random_char(5)
                save_ytdl_json_path = DOWNLOAD_LOCATION + f"/{message.from_user.id}{randem}.json"
                with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                    outfile.write(t_response)
                # Send the file to the user
                await client.send_document(
                    chat_id=message.chat.id,
                    document=save_ytdl_json_path,
                    caption="Here is the JSON data for the provided link.",
                    reply_to_message_id=message.reply_to_message.message_id
                )
            else:
                # If no JSON data is retrieved, notify the user
                await client.send_message(
                    chat_id=message.chat.id,
                    text="No JSON data found for the provided link.",
                    reply_to_message_id=message.reply_to_message.message_id
                )
        else:
            # If the replied message doesn't contain a link, notify the user
            await client.send_message(
                chat_id=message.chat.id,
                text="No link found in the replied message.",
                reply_to_message_id=message.reply_to_message.message_id
            )
    else:
        # If the message is not a reply, notify the user
        await client.send_message(
            chat_id=message.chat.id,
            text="Please reply to a message containing a link.",
            reply_to_message_id=message.message_id
        )
