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
async def button(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=script.START_TEXT.format(update.from_user.mention),
            reply_markup=script.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=script.HELP_TEXT,
            reply_markup=script.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=script.ABOUT_TEXT,
            reply_markup=script.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "opensettings":
        await update.answer()
        await opensettings(update.message)
    elif update.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(update.from_user.id)
        if not thumbnail:
            await update.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await update.answer()
            await bot.send_photo(
                update.message.chat.id,
                thumbnail, "Custom Thumbnail",
                reply_markup=types.InlineKeyboardMarkup(
                    [
                        [
                            types.InlineKeyboardButton("Delete Thumbnail", callback_data="deleteThumbnail")
                        ]
                    ]
                )
            )
    elif update.data == "deleteThumbnail":
        await db.set_thumbnail(update.from_user.id, None)
        await update.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await update.message.delete(True)
    elif update.data == "setThumbnail":
        await update.message.edit_text(
            text=script.TEXT,
            reply_markup=script.BUTTONS,
            disable_web_page_preview=True
        )

    elif update.data == "triggerUploadMode":
        await update.answer()
        upload_as_doc = await db.get_upload_as_doc(update.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(update.from_user.id, False)
        else:
            await db.set_upload_as_doc(update.from_user.id, True)
        await opensettings(update.message)
    elif "close" in update.data:
        await update.message.delete(True)

    elif "|" in update.data:
        await youtube_dl_call_back(bot, update)
    elif "=" in update.data:
        await ddl_call_back(bot, update)

    else:
        await update.message.delete()
