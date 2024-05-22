from pyrogram import Client, filters
from database.database import db
from info import ADMINS 
from utils import update_verify_status
import time
import datetime
import pytz

@Client.on_message(filters.command("update_me"))
async def update_user(bot, message):
    start_time = time.time()
    userid = message.from_user.id
    user = await bot.get_users(int(userid))
    sts = await message.reply_text('Updating user...')

    short_temp = "1"
    date_temp = "1999-12-31"
    time_temp = "23:59:59"
    
    await update_verify_status(bot, user.id, short_temp, date_temp, time_temp)

    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts.edit(f"User updated with default verification status.\nTime taken: {time_taken}")


@Client.on_message(filters.command("updateusers") & filters.user(ADMINS))
async def update_users_verifications(bot, message):
    sts = await message.reply_text('Updating users...')
    total_users = await db.total_users_count()
    start_time = time.time()
    count = 0
    complete = 0
    
    users = await db.get_all_users()
    
    async for user in users:
        user_id = user.get("id")
        short_temp = "1"
        date_temp = "1999-12-31"
        time_temp = "23:59:59"
        await update_verify_status(bot, user_id, short_temp, date_temp, time_temp)
        
        count += 1
        complete += 1
        
        if not complete % 20:
            await sts.edit(f"Total Users: {total_users}\nTotal Complete: {complete}\nTotal Complete Percentage: {complete/total_users*100:.2f}%")
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"All users updated with default verification status.\nTime taken: {time_taken}")
