import logging
import asyncio
import json
import os
import shutil
import time
from datetime import datetime
from pyrogram import enums
from info import *
from Script import script
from plugins.thumbnail import get_thumbnail, get_thumbnail_with_screenshot, get_metadata, get_width_and_duration, get_duration
from pyrogram.types import InputMediaPhoto
from plugins.functions.display_progress import progress_for_pyrogram, humanbytes
from database.database import db
from PIL import Image
from plugins.functions.ran_text import random_char

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


async def youtube_dl_call_back(client, message):
    cb_data = message.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext, random_suffix = cb_data.split("|")
    print(cb_data)
    random1 = random_char(5)

    save_ytdl_json_path = DOWNLOAD_LOCATION + \
        "/" + str(message.from_user.id) + f'{random_suffix}' + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except FileNotFoundError:
        await message.message.delete()
        return False

    youtube_dl_url = message.message.reply_to_message.text
    custom_file_name = str(response_json.get("title")) + \
        "_" + youtube_dl_format + "." + youtube_dl_ext
    youtube_dl_username = None
    youtube_dl_password = None

    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in message.message.reply_to_message.entities:
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

    if youtube_dl_username is not None:
        youtube_dl_username = youtube_dl_username.strip()
    if youtube_dl_password is not None:
        youtube_dl_password = youtube_dl_password.strip()

    logger.info(youtube_dl_url)
    logger.info(custom_file_name)

    await message.message.edit_caption(
        caption=script.DOWNLOAD_START.format(a=custom_file_name)
    )

    description = script.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]

    tmp_directory_for_each_user = DOWNLOAD_LOCATION + "/" + str(message.from_user.id) + f'{random1}'
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)

    download_directory = tmp_directory_for_each_user + "/" + custom_file_name

    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--bidi-workaround",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory
        ]
    else:
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", youtube_dl_format,
            "--bidi-workaround",
            youtube_dl_url,
            "-o", download_directory
        ]

    if HTTP_PROXY != "":
        command_to_exec.append("--proxy")
        command_to_exec.append(HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.append("--no-warnings")
    #command_to_exec.append("--geo-bypass-country")
    # command_to_exec.append("--quiet")
    logger.info(command_to_exec)
    start = datetime.now()
    
    downloaded_bytes = 0
    total_size = int(response_json.get("filesize"))  # Assuming file size available

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # ... other arguments
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Read process output in chunks
    while True:
        chunk = await process.stdout.read(1024)
        if not chunk:
            break
        downloaded_bytes += len(chunk)
        download_percentage = int((downloaded_bytes / total_size) * 100)

        # Update message caption with progress
        new_caption = f"**Progress:** {download_percentage}% ({humanbytes(downloaded_bytes)}/{humanbytes(total_size)})"
        await message.message.edit_caption(caption=new_caption)

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    logger.info(e_response)
    logger.info(t_response)
    ad_string_to_replace = "**Invalid link !**"
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await message.message.edit_caption(
            
            text=error_message
        )
        return False

    if os.path.exists(download_directory):
        end_one = datetime.now()
        time_taken_for_download = (end_one -start).seconds
        await message.message.edit_caption(
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
            await message.message.edit_caption(
                caption=script.RCHD_TG_API_LIMIT,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            start_time = time.time()
            if (await db.get_upload_as_doc(message.from_user.id)) is False:
                thumbnail = await get_thumbnail(client, message)
                await message.message.reply_document(
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        message.message,
                        start_time
                    )
                )
            else:
                width, height, duration = await get_metadata(download_directory)
                thumb_image_path = await get_thumbnail_with_screenshot(client, message, duration, download_directory)
                await message.message.reply_video(
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    thumb=thumb_image_path,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        message.message,
                        start_time
                    )
                )

            if tg_send_type == "audio":
                duration = await get_duration(download_directory)
                thumbnail = await get_thumbnail(client, message)
                await message.message.reply_audio(
                    audio=download_directory,
                    caption=description,
                    duration=duration,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        message.message,
                        start_time
                    )
                )
            elif tg_send_type == "vm":
                width, duration = await get_width_and_duration(download_directory)
                thumbnail = await get_thumbnail_with_screenshot(client, message, duration, download_directory)
                await message.message.reply_video_note(
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumbnail,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        script.UPLOAD_START,
                        message.message,
                        start_time
                    )
                )
            else:
                logger.info("✅ " + custom_file_name)

            end_two = datetime.now()
            time_taken_for_upload = (end_two - end_one).seconds
            try:
                shutil.rmtree(tmp_directory_for_each_user)
                os.remove(thumb_image_path)
            except:
                pass
                
            await message.message.edit_caption(
                caption=script.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload)
            )

            logger.info("✅ Downloaded in: " + str(time_taken_for_download))
            logger.info("✅ Uploaded in: " + str(time_taken_for_upload))
            
