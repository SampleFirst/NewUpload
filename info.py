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
VERIFY1_URL = environ.get('VERIFY1_URL', 'omnifly.in.net') #2nd p
VERIFY1_API = environ.get('VERIFY1_API', '579a68527328d450fea22397f9b8890c2e198cab') # ref from 1st p

VERIFY2_URL = environ.get('VERIFY2_URL', 'omnifly.in.net') # 2nd g
VERIFY2_API = environ.get('VERIFY2_API', '579a68527328d450fea22397f9b8890c2e198cab') # ref from 1st g

VERIFY3_URL = environ.get('VERIFY3_URL', 'omnifly.in.net') # 3rd p
VERIFY3_API = environ.get('VERIFY3_API', '7df51c1977b273b081a943eb2d4511e9227e1d66') # ref from 2nd p

VERIFY4_URL = environ.get('VERIFY4_URL', 'omnifly.in.net') # 3rd g
VERIFY4_API = environ.get('VERIFY4_API', '7df51c1977b273b081a943eb2d4511e9227e1d66') # ref form 2nd g

VERIFY5_URL = environ.get('VERIFY5_URL', 'omnifly.in.net') # 4th p
VERIFY5_API = environ.get('VERIFY5_API', '7df51c1977b273b081a943eb2d4511e9227e1d66') # ref from 3rd p


LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
PREMIUM_CHANNEL = int(environ.get('PREMIUM_CHANNEL', 0))
PREMIUM_CHAT = int(environ.get('PREMIUM_CHAT', 0))
BANNED_USERS = set(int(x) for x in environ.get("BANNED_USERS", "").split())
DOWNLOAD_LOCATION = "./DOWNLOADS"
UPDATE_CHANNEL = environ.get("UPDATE_CHANNEL", "")
MAX_FILE_SIZE = 50000000
TG_MAX_FILE_SIZE = 2097152000
FREE_USER_MAX_FILE_SIZE = 50000000
CHUNK_SIZE = int(environ.get("CHUNK_SIZE", 128))
DEF_THUMB_NAIL_VID_S = environ.get("DEF_THUMB_NAIL_VID_S", "https://placehold.it/90x90")
HTTP_PROXY = environ.get("HTTP_PROXY", "")
OUO_IO_API_KEY = ""
MAX_MESSAGE_LENGTH = 4096
PROCESS_MAX_TIMEOUT = 3700
DEF_WATER_MARK_FILE = "UploadLinkToFileBot"
DATABASE_URL = environ.get("DATABASE_URL", "")
TG_MIN_FILE_SIZE = 2097152000
BOT_USERNAME = environ.get("BOT_USERNAME", "")
PORT = int(environ.get("PORT", "8080"))
