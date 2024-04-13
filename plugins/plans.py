from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define the command handler
@Client.on_message(filters.command("plans"))
def plan(client, message):
    user_id = message.from_user.id
    name = message.from_user.mention 
    text = f"User ID: '{user_id}'\nName: {name}\n\n💠 Premium\n\n✅ Zee5 - Non-DRM Links Support\n✅ Voot - Non-DRM Links Support\n✅ SonyLIV - Non-DRM Links Support\n✅ DiscoveryPlusIndia - Non-DRM Links Support\n✅ AnimalPlanet - Non-DRM Links Support\n✅ AmazonMiniTV - Non-DRM Links Support\n✅ Mxplayer - Non-DRM Links Support\n✅ YouTube - Links Support\n✅ TikTok - Links Support\n\n✅ Other yt-dlp Supported Sites.\n\n✓ Validity: 1 MONTH\n\nAmount: 99 INR ₹\n\nBUY NOW FROM : @MyselfAstronaut"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("cancel", callback_data="cancel")
            ]
        ]
    )
    message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.MARKDOWN
    )
    
    
    
