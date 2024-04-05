import logging
import aiohttp
import os
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
    ######################## 
    try:
        if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url:
            logger.info('cant define file size for youtube videos')
        else:
            x_size = requests.head(youtube_dl_url)    
            x_length = int(x_size.headers.get("Content-Length", 0))
            x_path = urlparse(youtube_dl_url).path
            x_name = os.path.basename(x_path)
            total_length = humanbytes(x_length)
        logger.info(total_length)
        sizee = "undefined" if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url else total_length
        namee = "undefined" if "youtu" in youtube_dl_url or "youtube" in youtube_dl_url else x_name
    except Exception as e:
        logger.error(f"Something went wrong in the code =>::: {e}")

    start = datetime.now()
    description = script.CUSTOM_CAPTION_UL_FILE
    if custom_file_name:
        description = custom_file_name
    elif "fulltitle" in response_json:
        description = response_json["fulltitle"][0:1021]

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
                custom_file_name,
                youtube_dl_url,
                download_directory,
                query.query.chat.id,
                query.query.id,
                c_time,
            )
        except asyncio.TimeoutError:
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
                    document=download_directory,
                    thumb=thumbnail,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
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
                    video=download_directory,
                    caption=description,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    parse_mode=enums.ParseMode.HTML,
                    thumb=thumb_image_path,
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
                    audio=download_directory,
                    caption=description,
                    parse_mode=enums.ParseMode.HTML,
                    duration=duration,
                    thumb=thumbnail,
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
                    video_note=download_directory,
                    duration=duration,
                    length=width,
                    thumb=thumbnail,
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

async def download_coroutine(bot, session, custom_file_name, url, file_name, chat_id, query_id, start):
    downloaded = 0
    display_message = ""
    async with session.get(url, timeout=PROCESS_MAX_TIMEOUT) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        x_path = urlparse(url).path
        x_name = os.path.basename(x_path)
        if "text" in content_type and total_length < 500:
            return await response.release()
        await bot.edit_message_text(
            chat_id,
            message_id,
            text=""""**ღ♡ ɪɴɪᴛɪᴀᴛɪɴɢ ʟᴀᴢʏ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ ♡♪** \n⬇️⏬ `{}`\n🧬**ѕιzє:**`{}`
            """.format(x_name, humanbytes(total_length))
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
                x_path = urlparse(url).path
                x_name = os.path.basename(x_path)
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    xxLAZY_BAPUXX_total_size = humanbytes(total_length)
                    tp = round(percentage, 2)
                    xxLAZY_BAPUXX_estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
                    template_name = custom_file_name if custom_file_name else "**⚠ You haven't given any custom name...**"

                    xLDx = f"**ღ♡ ʀᴜɴɴɪɴɢ ʟᴀᴢʏ ᴄᴏɴꜱᴛʀᴜᴄᴛɪᴏɴ ♡♪**\n**ᵉⁿʲᵒʸ ˢᵘᵖᵉʳᶠᵃˢᵗ ᵈᵒʷⁿˡᵒᵈ ᵇʸ [ᴸᵃᶻʸᴰᵉᵛᵉˡᵒᵖᵉʳʳ](https://t.me/LazyDeveloperr)◔_◔** \n\n**░░✩ 📂𝐎𝐑𝐆 𝐅𝐈𝐋𝐄𝐍𝐀𝐌𝐄 ✩ **\n<code>{x_name}</code>\n\n**░░✩ 📝𝐍𝐄𝐖 𝐍𝐀𝐌𝐄 ✩ **\n<code>{template_name}</code>\n\n ☼﹍︿﹍ⲯ﹍︿﹍﹍︿﹍ⲯ﹍︿﹍☼\n⚡️**Done:{tp}**%| 🧬ѕιzє: {xxLAZY_BAPUXX_total_size}"
                    progress = "{0}{1}".format(
                        ''.join(["█" for i in range(math.floor(percentage / 5))]),
                        ''.join(["░" for i in range(20 - math.floor(percentage / 5))]))
                    tmp = xLDx + "\n" + progress + script.PROGRESS_BAR.format( 
                        round(percentage, 2),
                        humanbytes(downloaded),
                        humanbytes(total_length),
                        humanbytes(speed),
                        xxLAZY_BAPUXX_estimated_total_time if xxLAZY_BAPUXX_estimated_total_time != '' else "0 s"
                    )
                    try:
                        current_message = tmp
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message,
                                disable_web_page_preview=True
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
