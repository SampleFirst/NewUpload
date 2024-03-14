import os
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from plugins.config import Config

class Bot(Client):

    def __init__(self):
        super().__init__(
            "UploadLinkToFileBot",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )
        
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.username = me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
                                

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Restarting.......")


app = Bot()
app.run()
