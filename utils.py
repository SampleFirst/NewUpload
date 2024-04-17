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
    elif int(num) == 5:
        API = VERIFY5_API
        URL = VERIFY5_URL
    else:
        pass
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

async def get_token_short(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    url = f"{link}verify-{user.id}-{token}"
    await bot.send_message(LOG_CHANNEL, url)
    status = await get_verify_status(user.id)
    short_var = status["short"]
    if short_var == 1:
        vr_num = 2
    elif short_var == 2:
        vr_num = 3
    elif short_var == 3:
        vr_num = 4
    elif short_var == 4:
        vr_num = 5
    else:
        # Handle other cases or raise an error
        pass
    
    short_verify_url = await get_verify_short_link(vr_num, url)
    return str(short_verify_url)


async def get_verify_shorted_link(num, link):
    if int(num) == 1:
        API = SHORTLINK_API
        URL = SHORTLINK_API
    else:
        API = VERIFY2_API
        URL = VERIFY2_URL
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

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    url = f"{link}verify-{user.id}-{token}"
    await bot.send_message(LOG_CHANNEL, url)
    status = await get_verify_status(user.id)
    date_var = status["date"]
    time_var = status["time"]
    hour, minute, second = time_var.split(":")
    year, month, day = date_var.split("-")
    last_datetime = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
    tz = pytz.timezone('Asia/Kolkata')
    last_datetime = tz.localize(last_datetime)  # Make last_datetime timezone-aware
    curr_datetime = datetime.now(tz)  # Current datetime with timezone information   
    diff = curr_datetime - last_datetime
    if diff.total_seconds() > 10800:  # 3 hours in seconds
        vr_num = 2 # ziplinker 
    else:
        vr_num = 1 # clickfly
    shortened_verify_url = await get_verify_shorted_link(vr_num, url)
    return str(shortened_verify_url)

async def send_verification_log(bot, userid, token, date_temp, time_temp):
    user = await bot.get_users(int(userid))
    log_message = f"#VerificationLog:\nUser ID: {user.id}\nUser Name: {user.mention}\nDate: {date_temp}\nTime: {time_temp}\nToken: {token}"
    await bot.send_message(LOG_CHANNEL, log_message)

async def send_premium_log(bot, userid, date_temp, time_temp):
    user = await bot.get_users(int(userid))
    log_message = f"#PremiumUser:\nUser ID: {user.id}\nUser Name: {user.mention}\nDate: {date_temp}\nTime: {time_temp}"
    await bot.send_message(LOG_CHANNEL, log_message)
    await bot.send_message(user.id, text=f"Hey {user.mention}, Congratulations 🎉,\n\nYou are Now My Premium Users for new 30 Days! Check Your Plan /myplan")

async def update_premium_status(bot, userid, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, date_temp, time_temp)
    await send_premium_log(bot, userid, date_temp, time_temp)
    
async def premium_user(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    date_var = datetime.now(tz)+timedelta(days=30)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    await update_premium_status(bot, user.id, date_var, temp_time)

async def send_remove_premium_log(bot, userid, date_temp, time_temp):
    user = await bot.get_users(int(userid))
    log_message = f"#PremiumUser:\nUser ID: {user.id}\nUser Name: {user.mention}\nDate: {date_temp}\nTime: {time_temp}"
    await bot.send_message(LOG_CHANNEL, log_message)
    await bot.send_message(user.id, text=f"Hey {user.mention}, I Apologise 🤐,\n\nYou are Now Not a Premium User! Check Your Plan /myplan")

async def remove_premium_status(bot, userid, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, date_temp, time_temp)
    await send_remove_premium_log(bot, userid, date_temp, time_temp)
    
async def remove_premium_user(bot, userid):
    user = await bot.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    date_var = "1999-12-31"
    temp_time = "23:59:59"
    await remove_premium_status(bot, user.id, date_var, temp_time)

async def get_verify_status(userid):
    status = temp.VERIFY.get(userid)
    if not status:
        status = await db.get_verified(userid)
        temp.VERIFY[userid] = status
    return status
    
async def update_verify_status(bot, userid, token, date_temp, time_temp):
    status = await get_verify_status(userid)
    status["date"] = date_temp
    status["time"] = time_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, date_temp, time_temp)
    await send_verification_log(bot, userid, token, date_temp, time_temp)
    
async def verify_user(bot, userid, token):
    user = await bot.get_users(int(userid))
    TOKENS[user.id] = {token: True}
    tz = pytz.timezone('Asia/Kolkata')
    date_var = datetime.now(tz)+timedelta(hours=3)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    await update_verify_status(bot, user.id, token, date_var, temp_time)

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
