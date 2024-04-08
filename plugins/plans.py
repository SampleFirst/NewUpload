from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the command handler
@Client.on_message(filters.command("plans"))
def plan(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    text = f"User ID: {user_id}\nName: {name}\n\n💠 Premium\n\n✓ All Allowed URL\n✓ Task Limit: NO LIMIT\n✓ Time Gap: NO\n✓ No Anti-Spam Timer\n✓ Validity: 1 MONTH\n\nAmount: 99 INR ₹\n\nBUY NOW FROM : @UpcomingPaidBot"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("cancel", callback_data="cancel")
            ]
        ]
    )
    message.reply_text(text, reply_markup=keyboard)
