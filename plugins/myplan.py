from pyrogram import Client, filters
from datetime import datetime
from utils import *

@Client.on_message(filters.command("myplan") & filters.private)
async def myplan(client, message):
    userid = message.from_user.id

    verify_status = await get_verify_status(userid)
    expire_date = verify_status["date"]
    expire_time = verify_status["time"]
    
    current_datetime = datetime.now()
    expire_datetime = datetime.strptime(f"{expire_date} {expire_time}", "%Y-%m-%d %H:%M:%S")
    
    if expire_datetime < current_datetime:
        text = "Status: Plan Expired ❌\n"
        text += f"Expired on: {expire_date} {expire_time}"
    else:
        text = "Status: Active Premium Plan ✅\n"
        text += f"Expire Date: {expire_date}\n"
        text += f"Expire Time: {expire_time}\n"
    
    await message.reply_text(text)
