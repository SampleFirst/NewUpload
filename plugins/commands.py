import logging
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired
from database.database import db
from info import *
from Script import script 
from utils import *

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await client.send_message(
            LOG_CHANNEL,
               f"#NewUser\n<b>➲ Username:</b> {message.from_user.mention}\n<b>➲ ID:</b> <code>{message.from_user.id}</code>"
        )
    
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [[
            InlineKeyboardButton("Update Channel", url=invite_link.invite_link)
        ]]
        await client.send_message(
            chat_id=message.from_user.id,
            text="Please Join My 'Updates Channel' to use this Bot!\n\nDue to Telegram Users Traffic, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    buttons = (
        [
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
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
            
    await message.reply_text(
        text=script.START_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
    return
    
@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command("total_users") & filters.user(ADMINS))
async def total_users_command(_, message):
    total_users = await db.total_users_count()
    await message.reply(f"Total users: {total_users}")

@Client.on_message(filters.command('deletealldata') & filters.user(ADMINS))
async def delete_all_data(bot, message):
    buttons = (
        [
            [InlineKeyboardButton('Yes', callback_data="autodelete")],
            [InlineKeyboardButton('Cancel', callback_data="close_data")]
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
            
    await message.reply_text(
        'This will delete all.\nDo you want to continue?',
        reply_markup=reply_markup,
        quote=True,
    )

@Client.on_message(filters.command('help') & filters.private)
async def help(client, message):
    buttons = (
        [
            [InlineKeyboardButton('⛔️ Close', callback_data='close')]
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        text=script.HELP_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@Client.on_message(filters.command('about') & filters.private)
async def about(client, message):
    buttons = (
        [
            [InlineKeyboardButton('⛔️ Close', callback_data='close')]
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        text=script.ABOUT_TEXT.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
