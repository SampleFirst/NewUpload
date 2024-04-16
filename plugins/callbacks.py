import os
import logging
from pyrogram import Client, types
from database.database import db
from Script import script
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.settings.settings import opensettings
from plugins.dl_button import ddl_call_back
from plugins.button import youtube_dl_call_back
from plugins.token import token_accepted
from utils import temp

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_callback_query()
async def button(client, query):
    if query.data == "home":
        buttons = [
            [
                InlineKeyboardButton('⚙️ Settings', callback_data='opensettings')
            ],
            [
                InlineKeyboardButton('❔ Help', callback_data='help'),
                InlineKeyboardButton('👨‍🚒 About', callback_data='about')
            ],
            [
                InlineKeyboardButton('⛔️ Close', callback_data='close')
            ]
        ]
        await query.message.edit_text(
            text=script.START_TEXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    elif query.data == "help":
        buttons = [
            [
                InlineKeyboardButton('🏡 Home', callback_data='home'),
                InlineKeyboardButton('👨‍🚒 About', callback_data='about')
            ],
            [
                InlineKeyboardButton('⛔️ Close', callback_data='close')
            ]
        ]
        await query.message.edit_text(
            text=script.HELP_TEXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    elif query.data == "about":
        buttons = [
            [
                InlineKeyboardButton('❔ Help', callback_data='help'),
                InlineKeyboardButton('🏡 Home', callback_data='home')
            ],
            [
                InlineKeyboardButton('⛔️ Close', callback_data='close')
            ]
        ]
        await query.message.edit_text(
            text=script.ABOUT_TEXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    elif query.data == "opensettings":
        await query.answer()
        await opensettings(query.message)
    elif query.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(query.from_user.id)
        if not thumbnail:
            await query.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await query.answer()
            await client.send_photo(
                query.message.chat.id,
                thumbnail, "Custom Thumbnail",
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Delete Thumbnail", callback_data="deletethumbnail")
                        ]
                    ]
                )
            )
    elif query.data == "deletethumbnail":
        await db.set_thumbnail(query.from_user.id, None)
        await query.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await query.message.delete()
    elif query.data == "setthumbnail":
        buttons = [
            [
                InlineKeyboardButton('⛔️ Close', callback_data='close')
            ]
        ]
        await query.message.edit_text(
            text=script.TEXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
    elif query.data == "triggerUploadMode":
        await query.answer()
        upload_as_doc = await db.get_upload_as_doc(query.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(query.from_user.id, False)
        else:
            await db.set_upload_as_doc(query.from_user.id, True)
        await opensettings(query.message)
    elif query.data == "autodelete":
        await db.delete_all_data()
        await query.message.edit_text('Successfully Deleted All The Users Data.')
    elif "close" in query.data:
        await query.message.delete()
    elif "|" in query.data:
        await youtube_dl_call_back(client, query)
    elif "=" in query.data:
        await ddl_call_back(client, query)
    elif query.data == "verifying":
        link = temp.TOKEN_ACCEPTED.get(query.from_user.id)
        if link:
            awite token_accepted(client, query, link)
    else:
        await query.message.delete()
