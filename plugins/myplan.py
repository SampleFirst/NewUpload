from pyrogram import Client, filters
from datetime import datetime, timedelta
from utils import get_verify_status

@Client.on_message(filters.command("myplan") & Filters.private)
async def myplan(client, message):
    userid = message.from_user.id

    verify_status = await get_verify_status(userid)
    expire_date = verify_status["date"]
    expire_time = verify_status["time"]

    current_datetime = datetime.now()
    expire_datetime = datetime.strptime(f"{expire_date} {expire_time}", "%Y-%m-%d %H:%M:%S")

    if expire_datetime < current_datetime:
        text = "Status: Expired ❌\n\n"
        text += f"Expired on: {expire_date} {expire_time}"
    else:
        check_datetime = expire_datetime - timedelta(days=30)

        if check_datetime < current_datetime:
            text = "Status: Premium ✅\n\n"
            text += f"Premium Date: {check_datetime.date()}\n"
            text += f"Premium Time: {check_datetime.time()}\n\n"
            text += f"Expire Date: {expire_date}\n"
            text += f"Expire Time: {expire_time}\n\n"
        else:
            text = "Status: Not Premium ❌\n"
            text += f"Expired on: {expire_date} {expire_time}"

    await message.reply_text(text)
