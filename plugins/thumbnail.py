import logging
import random
import os
from PIL import Image
from plugins.script import Translation
from pyrogram import Client, filters
from plugins.functions.help_Nekmo_ffmpeg import take_screen_shot
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.functions.forcesub import handle_force_subscribe
from plugins.database.database import db
from plugins.config import Config
from plugins.settings.settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.photo)
async def save_photo(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
        if Config.UPDATES_CHANNEL:
            fsub = await handle_force_subscribe(bot, update)
            if fsub == 400:
                return

    # received single photo
    download_location = os.path.join(
        Config.DOWNLOAD_LOCATION,
        str(update.from_user.id) + ".jpg"
    )
    await bot.download_media(
        message=update,
        file_name=download_location
    )
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
    await db.set_thumbnail(update.from_user.id, thumbnail=update.photo.file_id)

@Client.on_message(filters.command(["deletethumbnail"]))
async def delete_thumbnail(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
        if Config.UPDATES_CHANNEL:
            fsub = await handle_force_subscribe(bot, update)
            if fsub == 400:
                return

    download_location = os.path.join(
        DOWNLOAD_LOCATION,
        str(update.from_user.id)
    )
    try:
        os.remove(download_location + ".jpg")
    except:
        pass
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=update.message_id
    )
    await db.set_thumbnail(update.from_user.id, thumbnail=None)

@Client.on_message(filters.command("showthumb"))
async def view_thumbnail(bot, update):
    if not update.from_user:
        return await update.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
        if Config.UPDATES_CHANNEL:
            fsub = await handle_force_subscribe(bot, update)
            if fsub == 400:
                return   

    thumbnail = await db.get_thumbnail(update.from_user.id)
    if thumbnail is not None:
        await bot.send_photo(
            chat_id=update.chat.id,
            photo=thumbnail,
            caption="Saved your thumbnail",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="deleteThumbnail")
                    ]
                ]
            ),
            reply_to_message_id=update.message_id
        )
    else:
        await update.reply_text(text="No thumbnail found.")

async def get_thumbnail(bot, update):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        img = Image.open(thumbnail)
        img = img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None
    return thumbnail

async def get_thumbnail_with_screenshot(bot, update, duration, download_directory):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        thumbnail = await take_screen_shot(download_directory, os.path.dirname(download_directory), random.randint(0, duration - 1))
    return thumbnail

async def get_metadata(download_directory):
    width = 0
    height = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
    return width, height, duration

async def get_width_and_duration(download_directory):
    width = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
    return width, duration

async def get_duration(download_directory):
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    return duration
    
