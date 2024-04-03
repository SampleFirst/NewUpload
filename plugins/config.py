import os
import logging



class Config(object):
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    API_ID = int(os.environ.get("API_ID", "10956858"))
    
    API_HASH = os.environ.get("API_HASH", "cceefd3382b44d4d85be2d83201102b7")
    
    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())
    
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    
    UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "")
    
    MAX_FILE_SIZE = 50000000
    
    TG_MAX_FILE_SIZE = 2097152000
    
    FREE_USER_MAX_FILE_SIZE = 50000000
    
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
    
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    
    OUO_IO_API_KEY = ""
    
    MAX_MESSAGE_LENGTH = 4096
    
    PROCESS_MAX_TIMEOUT = 0
    
    DEF_WATER_MARK_FILE = "UploadLinkToFileBot"
    
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    
    SESSION_NAME = os.environ.get("SESSION_NAME", "UploadLinkToFileBot")
    
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002014187177"))
    
    LOGGER = logging

    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1002014187177")
    
    OWNER_ID = int(os.environ.get("OWNER_ID", "5433924139"))
    
    TG_MIN_FILE_SIZE = 2097152000
    
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")

    VERIFY2_URL = os.environ.get('VERIFY2_URL', "mdisklink.link")
    VERIFY2_API = os.environ.get('VERIFY2_API', "a9710a537139aae48410ec2d414acf3f29d52345")
    SHORTLINK_URL = os.environ.get('SHORTLINK_URL', 'clicksfly.com')
    SHORTLINK_API = os.environ.get('SHORTLINK_API', 'b773b7f2ae617656e8c417464724ceb6cc978ee1')
    
