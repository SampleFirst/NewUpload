import logging
import asyncio
import random 
import re
import os
import pytz 
from datetime import datetime, timedelta, date, time
import string
import aiohttp
from database.database import db
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid, ChatAdminRequired
from info import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TOKENS = {}
SPL_TOKENS = {}
VERIFIED = {}
BANNED = {}

# temp db for banned 
class temp(object):
    VERIFY = {}
    ACTIVE_URL = {}
    TOKEN_ACCEPTED = {}
    STORE_ID = {}

async def is_subscribed(bot, query=None, userid=None):
    try:
        if userid == None and query != None:
            user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
        else:
            user = await bot.get_chat_member(AUTH_CHANNEL, int(userid))
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False

async def send_premium_log(bot, userid, shortnum, date_temp, time_temp):
    user = await bot.get_users(int(userid))
    log_message = f"#PremiumUser:\nUser ID: {user.id}\nUser Name: {user.mention}\nShortnum: {shortnum}\nDate: {date_temp}\nTime: {time_temp}"
    await bot.send_message(LOG_CHANNEL, log_message)
    await bot.send_message(user.id, text=f"Hey {user.mention}, Congratulations 🎉,\n\nYou are Now My Premium Users for new 30 Days! Check Your Plan /myplan")

async def update_premium_status(bot, userid, short_temp, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["short"] = short_temp
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, short_temp, date_temp, time_temp)
    await send_premium_log(bot, userid, short_temp, date_temp, time_temp)
    
async def premium_user(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    short_var = 1
    date_var = datetime.now(tz)+timedelta(days=30)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    await update_premium_status(bot, user.id, short_var, date_var, temp_time)

async def send_remove_premium_log(bot, userid, shortnum, date_temp, time_temp):
    user = await bot.get_users(int(userid))
    log_message = f"#PremiumUser:\nUser ID: {user.id}\nUser Name: {user.mention}\nShortnum: {shortnum}\nDate: {date_temp}\nTime: {time_temp}"
    await bot.send_message(LOG_CHANNEL, log_message)
    await bot.send_message(user.id, text=f"Hey {user.mention}, I Apologise 🤐,\n\nYou are Now Not a Premium User! Check Your Plan /myplan")

async def remove_premium_status(bot, userid, short_temp, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["short"] = short_temp
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, short_temp, date_temp, time_temp)
    await send_remove_premium_log(bot, userid, short_temp, date_temp, time_temp)
    
async def remove_premium_user(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    short_var = 1
    date_var = datetime.now(tz)-timedelta(hours=25)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    await remove_premium_status(bot, user.id, short_var, date_var, temp_time)

async def send_special_verify_log(bot, userid, short, date, time):
    user = await bot.get_users(int(userid))
    if short == 1:
        shortnum = 5
    else:
        shortnum = short - 1
    log_message = f"#SpecialLog:\nUser ID: {user.id}\nUser Name: {user.mention}\nShortNum: {shortnum}\nDate: {date}\nTime: {time}"
    await bot.send_message(LOG_CHANNEL, log_message)

async def send_verify_log(bot, userid, short, date, time):
    user = await bot.get_users(int(userid))
    if short == 1:
        shortnum = 5
    else:
        shortnum = short - 1
    log_message = f"#VerificationLog:\nUser ID: {user.id}\nUser Name: {user.mention}\nShortNum: {shortnum}\nDate: {date}\nTime: {time}"
    await bot.send_message(LOG_CHANNEL, log_message)

async def update_special_verify_status(bot, userid, short_temp, date_temp, time_temp):
    short = await get_verify_status(userid)
    short["short"] = short_temp
    short["date"] = date_temp
    short["time"] = time_temp
    temp.VERIFY_SHORT[userid] = short
    await db.update_verification(userid, short_temp, date_temp, time_temp)
    await send_special_verify_log(bot, userid, short_temp, date_temp, time_temp)

async def update_verify_status(bot, userid, short_temp, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["short"] = short_temp
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, short_temp, date_temp, time_temp)
    await send_verify_log(bot, userid, short_temp, date_temp, time_temp)
    
async def verify_special_user(bot, userid, token): #verify_special_frist_short_user
    user = await bot.get_users(int(userid))
    SPL_TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    short = await get_verify_status(user.id)
    short_var = short["short"]
    shortnum = int(short_var)
    if shortnum == 5:
        vrnum = 1
        date_var = datetime.now(tz)+timedelta(hours=24)
        temp_time = date_var.strftime("%H:%M:%S")
        date_var, time_var = str(date_var).split(" ")
    else:
        vrnum = shortnum + 1
        date_var = datetime.now(tz)
        temp_time = date_var.strftime("%H:%M:%S")
        date_var, time_var = str(date_var).split(" ")
    await update_special_verify_status(bot, user.id, vrnum, date_var, temp_time)

async def verify_user(bot, userid, token): #verify_short_user
    user = await bot.get_users(int(userid))
    TOKENS[user.id] = {token: True}
    short = await get_verify_status(user.id)
    tz = pytz.timezone('Asia/Kolkata')
    date_var = datetime.now(tz)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    short_var = short["short"]
    shortnum = int(short_var)
    if shortnum == 5:
        vrnum = 1
    else:
        vrnum = shortnum + 1
    await update_verify_status(bot, user.id, vrnum, date_var, temp_time)

async def check_special_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in SPL_TOKENS.keys():
        STKN = SPL_TOKENS[user.id]
        if token in STKN.keys():
            is_used = STKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False
        
async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False
        
async def get_verify_short_link(num, link):
    if int(num) == 1:
        API = VERIFY1_API
        URL = VERIFY1_URL
    elif int(num) == 2:
        API = VERIFY2_API
        URL = VERIFY2_URL
    elif int(num) == 3:
        API = VERIFY3_API
        URL = VERIFY3_URL
    elif int(num) == 4:
        API = VERIFY4_API
        URL = VERIFY4_URL
    else:
        API = VERIFY5_API
        URL = VERIFY5_URL
    https = link.split(":")[0]
    if "http" == https:
        https = "https"
        link = link.replace("http", https)

    if URL == "api.shareus.in":
        url = f"https://{URL}/shortLink"
        params = {"token": API,
                  "format": "json",
                  "link": link,
                  }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.json(content_type="text/html")
                    if data["status"] == "success":
                        return data["shortlink"]
                    else:
                        logger.error(f"Error: {data['message']}")
                        return f'https://{URL}/shortLink?token={API}&format=json&link={link}'

        except Exception as e:
            logger.error(e)
            return f'https://{URL}/shortLink?token={API}&format=json&link={link}'
    else:
        url = f'https://{URL}/api'
        params = {'api': API,
                  'url': link,
                  }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.json()
                    if data["status"] == "success":
                        return data["shortenedUrl"]
                    else:
                        logger.error(f"Error: {data['message']}")
                        if URL == 'clicksfly.com':
                            return f'https://{URL}/api?api={API}&url={link}'
                        else:
                            return f'https://{URL}/api?api={API}&link={link}'
        except Exception as e:
            logger.error(e)
            if URL == 'clicksfly.com':
                return f'https://{URL}/api?api={API}&url={link}'
            else:
                return f'https://{URL}/api?api={API}&link={link}'

async def get_special_token(bot, userid, link): #get_token_special_short
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    SPL_TOKENS[user.id] = {token: False}
    url = f"{link}sverify-{user.id}-{token}"
    await bot.send_message(LOG_CHANNEL, url)
    short = await get_verify_status(user.id)
    short_var = short["short"]
    short_num = int(short_var)
    if short_num == 5:
        vr_num = 1
        short_verify_url = await get_verify_short_link(vr_num, url)
    else:
        vr_num = short_num + 1
        short_verify_url = await get_verify_short_link(vr_num, url)
    return str(short_verify_url)
    
async def get_token(bot, userid, link): #get_token_short
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    url = f"{link}verify-{user.id}-{token}"
    await bot.send_message(LOG_CHANNEL, url)
    short = await get_verify_status(user.id)
    short_var = short["short"]
    short_num = int(short_var)
    if short_num == 5:
        vr_num = 1
        short_verify_url = await get_verify_short_link(vr_num, url)
    else:
        vr_num = short_num + 1
        short_verify_url = await get_verify_short_link(vr_num, url)
    return str(short_verify_url)
    
async def get_verify_status(userid):
    status = temp.VERIFY.get(userid)
    if not status:
        status = await db.get_verified(userid)
        temp.VERIFY[userid] = status
    return status
    
async def check_verification(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    curr_time = now.strftime("%H:%M:%S")
    hour1, minute1, second1 = curr_time.split(":")
    curr_time = time(int(hour1), int(minute1), int(second1))
    status = await get_verify_status(user.id)
    date_var = status["date"]
    time_var = status["time"]
    years, month, day = date_var.split('-')
    comp_date = date(int(years), int(month), int(day))
    hour, minute, second = time_var.split(":")
    comp_time = time(int(hour), int(minute), int(second))
    if comp_date<today:
        return False
    else:
        if comp_date == today:
            if comp_time<curr_time:
                return False
            else:
                return True
        else:
            return True
            
