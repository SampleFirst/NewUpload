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
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/c/2020858146/4")
VERIFY2_URL = environ.get('VERIFY2_URL', "clicksfly.com")
VERIFY2_API = environ.get('VERIFY2_API', "b773b7f2ae617656e8c417464724ceb6cc978ee1")
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'mdisklink.link')
SHORTLINK_API = environ.get('SHORTLINK_API', 'a9710a537139aae48410ec2d414acf3f29d52345')

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
PROCESS_MAX_TIMEOUT = 0
DEF_WATER_MARK_FILE = "UploadLinkToFileBot"
DATABASE_URL = environ.get("DATABASE_URL", "")
TG_MIN_FILE_SIZE = 2097152000
BOT_USERNAME = environ.get("BOT_USERNAME", "")
PORT = int(environ.get("PORT", "8080"))
