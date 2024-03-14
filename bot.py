import os
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)

from aiohttp import web
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from plugins import web_server
from plugins.config import Config

PORT = int(os.environ.get("PORT", "8080"))

class Bot(Client):

    def __init__(self):
        super().__init__(
            "UploadLinkToFileBot",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=150,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )
        
    async def start(self):
        # Create download directory if not exists
        if not os.path.isdir(Config.DOWNLOAD_LOCATION):
            os.makedirs(Config.DOWNLOAD_LOCATION)
        await super().start()
        me = await self.get_me()
        self.username = me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
                                
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Restarting.......")


app = Bot()
app.run()
