import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# Others
IS_VERIFY = is_enabled(environ.get('IS_VERIFY', 'True'), True)
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "")
VERIFY1_URL = environ.get('VERIFY1_URL', 'instantearn.in') #2nd p
VERIFY1_API = environ.get('VERIFY1_API', '667b11aeda738ac4c494084055faff1f636f8534')

VERIFY2_URL = environ.get('VERIFY2_URL', 'runurl.in') # first 
VERIFY2_API = environ.get('VERIFY2_API', '5ed6df09ca6970fb5809dd7b4388b19bc12e9bca')

VERIFY3_URL = environ.get('VERIFY3_URL', 'runurl.in') # third 
VERIFY3_API = environ.get('VERIFY3_API', '4333efb61c180fb738724bfbe54427ba1b666169')

VERIFY4_URL = environ.get('VERIFY4_URL', 'runurl.in') # fourth 
VERIFY4_API = environ.get('VERIFY4_API', 'd45daa443ecff47b5a4ebae3c803ee3da53a96f4')


LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
DOWNLOAD_LOCATION = "./DOWNLOADS"
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
FREE_USER_MAX_FILE_SIZE = 50000000
CHUNK_SIZE = int(environ.get("CHUNK_SIZE", 128))
DEF_THUMB_NAIL_VID_S = environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
HTTP_PROXY = environ.get("HTTP_PROXY", "")
MAX_MESSAGE_LENGTH = 4096
PROCESS_MAX_TIMEOUT = 3700
DEF_WATER_MARK_FILE = "UploadLinkToFileBot"
DATABASE_URL = environ.get("DATABASE_URL", "")
TG_MIN_FILE_SIZE = 2097152000
PORT = int(environ.get("PORT", "8080"))
