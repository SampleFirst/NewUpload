import os
import logging
import logging.config
import pytz

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)

from aiohttp import web
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from datetime import date, datetime 
from plugins import web_server
from info import *
from Script import script 

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            bot_token=BOT_TOKEN,
            api_id=API_ID,
            api_hash=API_HASH,
            workers=150,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )
        
    async def start(self):
        # Create download directory if not exists
        if not os.path.isdir(DOWNLOAD_LOCATION):
            os.makedirs(DOWNLOAD_LOCATION)
        await super().start()
        me = await self.get_me()
        U_NAME = me.username
        self.username = me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(a=today, b=time, c=U_NAME))

        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Restarting.......")


app = Bot()
app.run()
