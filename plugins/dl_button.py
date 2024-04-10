import logging
import aiohttp
import os
import asyncio
import shutil
import time
import requests
from urllib.parse import urlparse
from datetime import datetime
from pyrogram import enums 
from pyrogram.types import Message
from info import *
from Script import script 
from plugins.thumbnail import get_thumbnail, get_thumbnail_with_screenshot, get_metadata, get_width_and_duration, get_duration
from database.database import db
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
from hachoir.parser import createParser
from PIL import Image

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def ddl_call_back(client, query):
    logger.info(query)
    cb_data = query.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("=")
    thumb_image_path = DOWNLOAD_LOCATION + \
        "/" + str(query.from_user.id) + ".jpg"
    youtube_dl_url = query.message.reply_to_message.text
    custom_file_name = os.path.basename(youtube_dl_url)
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        else:
            for entity in query.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    l = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + l]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940
        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in query.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    user = await client.get_me()
    mention = user["mention"]
    description = script.CUSTOM_CAPTION_UL_FILE.format(mention)
    start = datetime.now()
    await query.message.edit_caption(
        caption=script.DOWNLOAD_START,
        parse_mode=enums.ParseMode.HTML
    )
    tmp_directory_for_each_user = DOWNLOAD_LOCATION + "/" + str(query.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    async with aiohttp.ClientSession() as session:
        c_time = time.time()
        try:
            await download_coroutine(
                client,
                session,
                youtube_dl_url,
                download_directory,
                query.message.chat.id,
                query.id,
                c_time
            )
        except asyncio.TimeOutError:
            await query.message.edit_caption(
                caption=script.SLOW_URL_DECED,
                parse_mode=enums.ParseMode.HTML
            )
            return False
    if os.path.exists(download_directory):
        end_one = datetime.now()
        await query.message.edit_caption(
            caption=script.UPLOAD_START,
            parse_mode=enums.ParseMode.HTML
        )
        file_size = TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if file_size > TG_MAX_FILE_SIZE:
            await query.message.edit_caption(
                
                caption=script.RCHD_TG_API_LIMIT,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            
            start_time = time.time()
            if (await db.get_upload_as_doc(query.from_user.id)) is False:
                thumbnail = await get_thumbnail(client, query)
                await query.message.reply_document(
                    #chat_id=query.message.chat.id,
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    #reply_to_message_id=query.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        query.message,
                        start_time
                    )
                )
            else:
                 width, height, duration = await get_metadata(download_directory)
                 thumb_image_path = await get_thumbnail_with_screenshot(client, query, duration, download_directory)
                 await query.message.reply_video(
                    #chat_id=query.message.chat.id,
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumb_image_path,
                    #reply_to_message_id=query.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        query.message,
                        start_time
                    )
                )
            if tg_send_type == "audio":
                duration = await get_duration(download_directory)
                thumbnail = await get_thumbnail(client, query)
                await query.message.reply_audio(
                    #chat_id=query.message.chat.id,
                    audio=download_directory,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    duration=duration,
                    thumb=thumbnail,
                    #reply_to_message_id=query.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        query.message,
                        start_time
                    )
                )
            elif tg_send_type == "vm":
                width, duration = await get_width_and_duration(download_directory)
                thumbnail = await get_thumbnail_with_screenshot(client, query, duration, download_directory)
                await query.message.reply_video_note(
                    #chat_id=query.message.chat.id,
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumbnail,
                    #reply_to_message_id=query.id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        query.message,
                        start_time
                    )
                )
            else:
                logger.info("Did this happen? :\\")
            end_two = datetime.now()
            try:
                os.remove(download_directory)
                os.remove(thumb_image_path)
            except:
                pass
            time_taken_for_download = (end_one - start).seconds
            time_taken_for_upload = (end_two - end_one).seconds
            await query.message.edit_caption(
                caption=script.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload),
               
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await query.message.edit_caption(
            caption=script.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
            
            
            parse_mode=enums.ParseMode.HTML
        )

async def download_coroutine(client, session, url, file_name, chat_id, message_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await query.message.edit_caption(
         
      
            caption="""Initiating Download
**🔗 Uʀʟ :** `{}`
**🗂️ Sɪᴢᴇ :** {}""".format(url, humanbytes(total_length)),
            parse_mode=enums.ParseMode.HTML
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**DᴏᴡɴʟᴏᴀᴅɪɴG**
**🔗 Uʀʟ :** `{}`

**🗂️ Sɪᴢᴇ :** {}

**✅ Dᴏɴᴇ :** {}

**⏱️ Eᴛᴀ :** {}""".format(
    url,
    humanbytes(total_length),
    humanbytes(downloaded),
    TimeFormatter(estimated_total_time)
)
                        if current_message != display_message:
                            await query.message.edit_caption(
                                caption=current_message,
                                parse_mode=enums.ParseMode.HTML
            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
