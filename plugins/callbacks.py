import os
import logging
from pyrogram import Client, types
from database.database import db
from Script import script 
from plugins.settings.settings import opensettings
from plugins.dl_button import ddl_call_back
from plugins.button import youtube_dl_call_back

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_callback_query()
async def button(client, query):
    if query.data == "home":
        await query.message.edit_text(
            text=script.START_TEXT.format(query.from_user.mention),
            reply_markup=script.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "help":
        await query.message.edit_text(
            text=script.HELP_TEXT,
            reply_markup=script.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif query.data == "about":
        await query.message.edit_text(
            text=script.ABOUT_TEXT,
            reply_markup=script.ABOUT_BUTTONS,
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
                            types.InlineKeyboardButton("Delete Thumbnail", callback_data="deleteThumbnail")
                        ]
                    ]
                )
            )
    elif query.data == "deleteThumbnail":
        await db.set_thumbnail(query.from_user.id, None)
        await query.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await query.message.delete(True)
    elif query.data == "setThumbnail":
        await query.message.edit_text(
            text=script.TEXT,
            reply_markup=script.BUTTONS,
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
    elif "close" in query.data:
        await query.message.delete(True)
    elif "|" in update.data:
        await youtube_dl_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)
    else:
        await update.message.delete()


    
