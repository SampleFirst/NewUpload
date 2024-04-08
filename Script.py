from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class script(object):

    START_TEXT = """
👋 ʜᴇʏ {} 

ɪ ᴀᴍ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴜʀʟ ᴜᴘʟᴏᴀᴅᴇʀ ʙᴏᴛ.

ꜱᴇɴᴅ ᴍᴇ ᴀ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ ᴀɴᴅ ɪ ᴡɪʟʟ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴀꜱ ᴀ ꜰɪʟᴇ/ᴠɪᴅᴇᴏ.

ᴜꜱᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴍᴇ.
"""
    HELP_TEXT = """
**Link to Media or File**
➠ Send a link for upload to Telegram file or media.

**Set Thumbnail**
➠ Send a photo to make it as permanent thumbnail.

**Deleting Thumbnail**
➠ Send /delthumb to delete thumbnail.

**Settings**
➠ Configure my settings to change upload mode.

**Show Thumbnail**
➠ Send /showthumb to view custom thumbnail. 
"""
    ABOUT_TEXT = """
**Name** : [Uploader Bot v4](https://t.me/BraveLinkToFileBot)

**Channel** : [Update Channel](https://t.me/+pXzjJ61z81IyMGFl)

**Support Group** : [Support Chat](https://t.me/+rFmrUic07f9iMjM1)

**Language:** [Python 3.12.2](https://www.python.org/)

**Framework:** [Pyrogram 2.0.106](https://docs.pyrogram.org/)
"""

    PROGRESS = """
╭━━❰ PROGRESS BAR ❱━━➣
┣⪼ ✅ : {1}
┣⪼ ⏳️ : {2}
┣⪼ 🚀 : {3}/s
┣⪼ ⏱️ : {4}
╰━━━━━━━━━━━━━━━━━➣ 
"""

    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙️ Settings', callback_data='opensettings')
        ],[
        InlineKeyboardButton('❔ Help', callback_data='help'),
        InlineKeyboardButton('👨‍🚒 About', callback_data='about')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡 Home', callback_data='home'),
        InlineKeyboardButton('👨‍🚒 About', callback_data='about')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏡 Home', callback_data='home'),
        InlineKeyboardButton('❔ Help', callback_data='help')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
    BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
    TEXT = "Send me any custom thumbnail to set it"
    IFLONG_FILE_NAME = " Only 64 characters can be named . "
    RENAME_403_ERR = "Sorry. You are not permitted to rename this file."
    ABS_TEXT = " Please don't be selfish."
    FORMAT_SELECTION = "Now Select The Desired Format or File 🗄️ Size to Upload"
    SET_CUSTOM_USERNAME_PASSWORD = """"""
    NOYES_URL = "URL detected. Please use https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    DOWNLOAD_START = "Downloading Please Wait ⏳\n\n{a}"
    UPLOAD_START = "📤 Uploading Please Wait"
    RCHD_BOT_API_LIMIT = "size greater than maximum allowed size (50MB). Neverthless, trying to upload."
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG = " OWNER: Admin 💕\nFor the List of Telegram Bots"
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in {} seconds.\n\nUploaded in {} seconds"
    NOT_AUTH_USER_TEXT_FILE_SIZE = "Detected File Size: {}. Free Users can only upload: {}\nPlease /upgrade your subscription.\nIf you think this is a bug, please contact Admin"
    SAVED_CUSTOM_THUMB_NAIL = "Custom video/file thumbnail saved. This image will be used in the video/file."
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ Custom thumbnail cleared successfully"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared successfully."
    SAVED_RECVD_DOC_FILE = "Document Downloaded Successfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_CUSTOM_THUMB_NAIL_FOUND = "No custom thumbnail found"
    NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"
    FILE_NOT_FOUND = "Error, File not Found!!"
    USER_ADDED_TO_DB = "User <a href='tg://user?id={}'>{}</a> added to {} till {}."
    SOMETHING_WRONG = "<code>Something Wrong. Try again.</code>"
    REPLY_TO_DOC_GET_LINK = "Reply to a Telegram media to get High Speed Direct Download Link"
    REPLY_TO_DOC_FOR_C2V = "Reply to a Telegram media to convert"
    REPLY_TO_DOC_FOR_SCSS = "Reply to a Telegram media to get screenshots"
    REPLY_TO_DOC_FOR_RENAME_FILE = "Reply to a Telegram media to /ren with custom thumbnail support"
    AFTER_GET_GOFILE_LINK = " <b>File Name :</b> <code>{}</code>\n<b>File Size :</b> {}\n<b>File MD5 Checksum :</b> <code>{}</code>\n\n<b>⚡Link⚡ :</b> <code>{}</code>\n\n Valid until 10 days of inactivity"
    FF_MPEG_RO_BOT_RE_SURRECT_ED = """Syntax: /trim HH:MM:SS for screenshot of that specific time."""
    FF_MPEG_RO_BOT_STEP_TWO_TO_ONE = "First send /downloadmedia to any media so that it can be downloaded to my local. \nSend /storageinfo to know the media, that is currently downloaded."
    FF_MPEG_RO_BOT_STOR_AGE_INFO = "Video Duration: {}\nSend /clearffmpegmedia to delete this media, from my storage.\nSend /trim HH:MM:SS [HH:MM:SS] to cut a small photo/video, from the above media."
    FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS = "A saved media already exists. Please send /storageinfo to know the current media details."
    USER_DELETED_FROM_DB = "User <a href='tg://user?id={}'>{}</a> deleted from DataBase."
    REPLY_TO_DOC_OR_LINK_FOR_RARX_SRT = "Reply to a Telegram media (MKV), to extract embedded streams"
    REPLY_TO_MEDIA_ALBUM_TO_GEN_THUMB = "Reply /generatecustomthumbnail to a media album, to generate custom thumbnail"
    ERR_ONLY_TWO_MEDIA_IN_ALBUM = "Media Album should contain only two photos. Please re-send the media album, and then try again, or send only two photos in an album."
    INVALID_UPLOAD_BOT_URL_FORMAT = "URL format is incorrect. Make sure your url starts with either http:// or https://. You can set custom file name using the format link | file_name.extension"
    ABUSIVE_USERS = "You are not allowed to use this bot. If you think this is a mistake, please check /me to remove this restriction."
    FF_MPEG_RO_BOT_AD_VER_TISE_MENT = "Join : @iPepkornBots \n For the list of Telegram bots. "
    EXTRACT_ZIP_INTRO_ONE = "Send a compressed file first, Then reply /unzip command to the file."
    EXTRACT_ZIP_INTRO_THREE = "Analyzing received file. ⚠️ This might take some time. Please be patient. "
    UNZIP_SUPPORTED_EXTENSIONS = ("zip", "rar")
    EXTRACT_ZIP_ERRS_OCCURED = "Sorry. Errors occurred while processing compressed file. Please check everything again twice, and if the issue persists, report this to <a href='https://telegram.dog/ThankTelegram'>@SpEcHlDe</a>"
    CANCEL_STR = "Process Cancelled"
    ZIP_UPLOADED_STR = "Uploaded {} files in {} seconds"
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
    FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"
    BANNED_USER_TEXT = "<code>You are Banned!</code>"
    CHECK_LINK = "Processing your link ⌛"
    RESTART_TXT = "#Restarted\n\n🔄 Bot Restarted!\n📅 Date: <code>{a}</code>\n⏰ Time: <code>{b}</code>\n🌐 Timezone: <code>Asia/Kolkata</code>\n\n#{c}\n#Restart_{c}"

