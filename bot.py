import os
import logging
import logging.config

from plugins.config import Config
from pyrogram import Client as Ntbots
from pyrogram import filters

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.WARNING)


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    Ntbots = Ntbots(
        "UploadLinkToFileBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins)
    Ntbots.run()

