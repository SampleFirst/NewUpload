import logging
import asyncio
import json
import time
from pyrogram import Client, enums, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Thumbnail
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from utils import is_subscribed, check_verification
from info import *
from Script import script 
from plugins.functions.display_progress import humanbytes
from plugins.functions.help_uploadbot import DownLoadFile
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from plugins.functions.ran_text import random_char

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.private & filters.regex(pattern=".*https.*"))
async def echo(client, message):
    if LOG_CHANNEL:
        try:
            log_info = "Message Sender Information\n"
            log_info += "\nFirst Name: " + message.from_user.first_name
            log_info += "\nUser ID: " + str(message.from_user.id)
            log_info += "\nUsername: @" + message.from_user.username if message.from_user.username else ""
            log_info += "\nText Link: " + message.text 
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=log_info,
                disable_web_page_preview=True
            )
        except Exception as error:
            print(error)
            
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Mᴀᴋᴇ sᴜʀᴇ Bᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ Fᴏʀᴄᴇsᴜʙ ᴄʜᴀɴɴᴇʟ")
            return
        btn = [[
            InlineKeyboardButton("Update Channel", url=invite_link.invite_link)
        ]]
        await client.send_message(
            chat_id=message.from_user.id,
            text="Please Join My Updates Channel to use this Bot!\n\nDue to Telegram Users Traffic, Only Channel Subscribers can use the Bot!\n\nNote: Once you join the update channel, do not leave to avoid being banned.",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    if IS_VERIFY and not await check_verification(client, message.from_user.id):
        await client.send_message(
            chat_id=message.from_user.id,
            text="Upgrade to our plan for use this bot\n\n Use /plan for Show Premium Plan Features\n\n Use /send for Contect Admin For *reply any text or photo bot send to Admin",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return 
    else:
        logger.info(message.from_user)
        url = message.text
        youtube_dl_username = None
        youtube_dl_password = None
        file_name = None
    
        print(url)
        if "|" in url:
            url_parts = url.split("|")
            if len(url_parts) == 2:
                url = url_parts[0]
                file_name = url_parts[1]
            elif len(url_parts) == 4:
                url = url_parts[0]
                file_name = url_parts[1]
                youtube_dl_username = url_parts[2]
                youtube_dl_password = url_parts[3]
            else:
                for entity in message.entities:
                    if entity.type == "text_link":
                        url = entity.url
                    elif entity.type == "url":
                        o = entity.offset
                        l = entity.length
                        url = url[o:o + l]
            if url is not None:
                url = url.strip()
            if file_name is not None:
                file_name = file_name.strip()
            # https://stackoverflow.com/a/761825/4723940
            if youtube_dl_username is not None:
                youtube_dl_username = youtube_dl_username.strip()
            if youtube_dl_password is not None:
                youtube_dl_password = youtube_dl_password.strip()
            logger.info(url)
            logger.info(file_name)
        else:
            for entity in message.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if HTTP_PROXY != "":
            command_to_exec = [
                "yt-dlp",
                "--no-warnings",
                "--youtube-skip-hls-manifest",
                "-j",
                url,
                "--proxy", HTTP_PROXY
            ]
        else:
            command_to_exec = [
                "yt-dlp",
                "--no-warnings",
                "--youtube-skip-hls-manifest",
                "-j",
                url
            ]
        if youtube_dl_username is not None:
            command_to_exec.append("--username")
            command_to_exec.append(youtube_dl_username)
        if youtube_dl_password is not None:
            command_to_exec.append("--password")
            command_to_exec.append(youtube_dl_password)
        logger.info(command_to_exec)
        chk = await client.send_message(
                chat_id=message.chat.id,
                text=f'Processing your link ⌛',
                disable_web_page_preview=True,
                reply_to_message_id=message.id,
                parse_mode=enums.ParseMode.HTML
              )
        process = await asyncio.create_subprocess_exec(
            *command_to_exec,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        logger.info(e_response)
        t_response = stdout.decode().strip()
        if e_response and "nonnumeric port" not in e_response:
            error_message = e_response.replace("please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to message. Be sure to call youtube-dl with the --verbose flag and include its complete output.", "")
            if "This video is only available for registered users." in error_message:
                error_message += script.SET_CUSTOM_USERNAME_PASSWORD
            await chk.delete()
            await asyncio.sleep(2)
            await client.send_message(
                chat_id=message.chat.id,
                text=script.NO_VOID_FORMAT_FOUND.format(str(error_message)),
                reply_to_message_id=message.id,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True
            )
            return False
        if t_response:
            x_response_parts = t_response.split("\n")
            x_response = x_response_parts[0] if x_response_parts else ""
            response_json = json.loads(x_response)
            randem = random_char(5)
            save_ytdl_json_path = DOWNLOAD_LOCATION + \
                "/" + str(message.from_user.id) + f'{randem}' + ".json"
            with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
                json.dump(response_json, outfile, ensure_ascii=False)
            inline_keyboard = []
            duration = response_json.get("duration")
            if "formats" in response_json:
                for formats in response_json["formats"]:
                    format_id = formats.get("format_id")
                    format_string = formats.get("format_note") or formats.get("format")
                    format_ext = formats.get("ext")
                    approx_file_size = humanbytes(formats.get("filesize", 0))
                    cb_string_video = "{}|{}|{}|{}".format(
                        "video", format_id, format_ext, randem)
                    cb_string_file = "{}|{}|{}|{}".format(
                        "file", format_id, format_ext, randem)
                    ikeyboard = [
                        InlineKeyboardButton("📂 " + format_string + " " + format_ext + " " + approx_file_size + " ", callback_data=(cb_string_video).encode("UTF-8"))
                    ] if "audio only" not in format_string else [
                        InlineKeyboardButton("📦 [" + "] ( " + approx_file_size + " )", callback_data=(cb_string_video).encode("UTF-8"))
                    ]
                    inline_keyboard.append(ikeyboard)
                if duration is not None:
                    inline_keyboard.extend([
                        [
                            InlineKeyboardButton("🎵 ᴍᴘ𝟹 " + "(" + "64 ᴋʙᴘs" + ")", callback_data=("audio|64k|mp3|" + randem).encode("UTF-8")),
                            InlineKeyboardButton("🎵 ᴍᴘ𝟹 " + "(" + "128 ᴋʙᴘs" + ")", callback_data=("audio|128k|mp3|" + randem).encode("UTF-8"))
                        ],
                        [
                            InlineKeyboardButton("🎵 ᴍᴘ𝟹 " + "(" + "320 ᴋʙᴘs" + ")", callback_data=("audio|320k|mp3|" + randem).encode("UTF-8"))
                        ],
                        [
                            InlineKeyboardButton("⛔️ ᴄʟᴏsᴇ", callback_data='close'.encode("UTF-8"))               
                        ]
                    ])
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await chk.delete()
            await client.send_message(
                chat_id=message.chat.id,
                text=script.FORMAT_SELECTION.format(Thumbnail) + "\n" + script.SET_CUSTOM_USERNAME_PASSWORD,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            inline_keyboard = [
                [
                    InlineKeyboardButton("🎬 ᴍᴇᴅɪᴀ", callback_data=("video|LFO|NONE|" + randem).encode("UTF-8"))
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)
            await chk.delete(True)
            await client.send_message(
                chat_id=message.chat.id,
                text=script.FORMAT_SELECTION,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
