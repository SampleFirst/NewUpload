import os
import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)

from info import *
from pyrogram import Client as Ntbots
from pyrogram import filters


if __name__ == "__main__" :

    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    plugins = dict(root="plugins")
    Ntbots = Ntbots(
        "UploadLinkToFileBot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins)

    print("🎊 I AM ALIVE 🎊")
    Ntbots.run()

