import os
import logging
import logging.config
from plugins.config import Config
from pyrogram import Client as Ntbots
from pyrogram import filters, __version__
from pyrogram.raw.all import layer

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class Bot(Ntbots):
    def __init__(self):
        super().__init__(
            "UploadLinkToFileBot",
            bot_token=Config.BOT_TOKEN,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            plugins={"root": "plugins"},
            workers=50,
            sleep_threshold=5
        )

    async def start(self):
        # Create download directory if not exists
        if not os.path.isdir(Config.DOWNLOAD_LOCATION):
            os.makedirs(Config.DOWNLOAD_LOCATION)
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")


# Start the bot
app = Bot()
app.run()
