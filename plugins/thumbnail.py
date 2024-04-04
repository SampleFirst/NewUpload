import logging
import random
import os
from PIL import Image
from Script import script 
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from plugins.functions.help_Nekmo_ffmpeg import take_screen_shot
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.database import db
from info import *
from utils import is_subscribed, check_verification, get_token
from plugins.settings.settings import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.photo)
async def save_photo(client, message):
    if not message.from_user:
        return await message.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        if AUTH_CHANNEL and not await is_subscribed(client, message):
            try:
                invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
            except ChatAdminRequired:
                logger.error("Mᴀᴋᴇ sᴜʀᴇ Bᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ Fᴏʀᴄᴇsᴜʙ ᴄʜᴀɴɴᴇʟ")
                return
            btn = [[InlineKeyboardButton("❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆", url=invite_link.invite_link)]]
    
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ᴏᴜʀ Bᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ...\n\nIғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴀɴᴅ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '↻ Tʀʏ Aɢᴀɪɴ' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ...\n\nTʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ғɪʟᴇs...**",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=enums.ParseMode.MARKDOWN
                )
            return
    
        if IS_VERIFY and not await check_verification(client, message.from_user.id):
            btn = [[
                InlineKeyboardButton("Verify", url=await get_token(client, message.from_user.id, "https://telegram.me/BraveLinkToFileBot?start="))
            ]]
            await client.send_message(
                chat_id=message.from_user.id,
                text="<b>You are not verified!\nKindly verify to continue so that you can get access to unlimited movies until  3 hours from now!</b>",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            return 
    
    # received single photo
    download_location = os.path.join(
        DOWNLOAD_LOCATION,
        str(message.from_user.id) + ".jpg"
    )
    await client.download_media(
        message=message,
        file_name=download_location
    )
    await client.send_message(
        chat_id=message.chat.id,
        text=script.SAVED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=message.id
    )
    await db.set_thumbnail(message.from_user.id, thumbnail=message.photo.file_id)

@Client.on_message(filters.command(["deletethumbnail"]))
async def delete_thumbnail(client, message):
    if not message.from_user:
        return await message.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        if AUTH_CHANNEL:
            fsub = await handle_force_subscribe(client, message)
            if fsub == 400:
                return

    download_location = os.path.join(
        DOWNLOAD_LOCATION,
        str(message.from_user.id)
    )
    try:
        os.remove(download_location + ".jpg")
    except:
        pass
    await client.send_message(
        chat_id=message.chat.id,
        text=script.DEL_ETED_CUSTOM_THUMB_NAIL,
        reply_to_message_id=message.id
    )
    await db.set_thumbnail(message.from_user.id, thumbnail=None)

@Client.on_message(filters.command("showthumb"))
async def view_thumbnail(client, message):
    if not message.from_user:
        return await message.reply_text("I don't know about you, sir.")
    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        if AUTH_CHANNEL:
            fsub = await handle_force_subscribe(client, message)
            if fsub == 400:
                return   

    thumbnail = await db.get_thumbnail(message.from_user.id)
    if thumbnail is not None:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=thumbnail,
            caption="Saved your thumbnail",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗑️ Delete Thumbnail", callback_data="deleteThumbnail")
                    ]
                ]
            ),
            reply_to_message_id=message.id
        )
    else:
        await message.reply_text(text="No thumbnail found.")

async def get_thumbnail(client, message):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(message.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(message.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await client.download_media(message=db_thumbnail, file_name=thumb_image_path)
        img = Image.open(thumbnail)
        img = img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None
    return thumbnail

async def get_thumbnail_with_screenshot(client, message, duration, download_directory):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(message.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(message.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await client.download_media(message=db_thumbnail, file_name=thumb_image_path)
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
    
