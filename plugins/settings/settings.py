import asyncio
from pyrogram import types, errors, enums
from database.database import db

async def open_settings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from the database!")
        return

    upload_as_doc = user_data.get("upload_as_doc", False)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)

    buttons_markup = [
        [types.InlineKeyboardButton(f"Upload as {'🎥 Video' if upload_as_doc else '🗃️ File'}",
                                    callback_data="triggerUploadMode")],
        [types.InlineKeyboardButton(f"{'Change' if thumbnail else 'Set'} Thumbnail",
                                    callback_data="setThumbnail")]
    ]

    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("Show Thumbnail",
                                                          callback_data="showThumbnail")])

    buttons_markup.append([types.InlineKeyboardButton("Close",
                                                      callback_data="close")])

    try:
        await m.edit(
            text="**Here you can setup your settings**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    except errors.MessageNotModified:
        pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await open_settings(m)
    except Exception as err:
        print(f"An error occurred: {err}")

# Note: I've made some variable names lowercase for consistency and PEP 8 compliance.
