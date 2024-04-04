from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the command handler
@Client.on_message(filters.command("plan"))
def plan(client, message):
    text = "Per Month: 99 Rupees\n"
    text += "All Allowed Links\n"
    text += "No Timeouts\n"
    text += "No Links Limit\n\n"
    text += "Ask for QR code /send \n"
    text += "Note: Payment Not Refundable"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("cancel", callback_data="cancel")
            ]
        ]
    )
    message.reply_text(text, reply_markup=keyboard)

