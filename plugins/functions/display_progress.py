import math
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import enums
from Script import script 

async def progress_for_pyrogram(current, total, ud_type, query, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time_ms = round(diff) * 1000
        time_to_completion_ms = round((total - current) / speed) * 1000
        estimated_total_time_ms = elapsed_time_ms + time_to_completion_ms

        elapsed_time = TimeFormatter(elapsed_time_ms)
        estimated_total_time = TimeFormatter(estimated_total_time_ms)

        progress_bar = "[" + ''.join(["█" for _ in range(math.floor(percentage / 5))]) + \
                       ''.join(["" for _ in range(20 - math.floor(percentage / 5))]) + "]"

        progress_text = script.PROGRESS.format(
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )

        try:
            await query.edit(
                text=f"**{ud_type}**\n\n{progress_bar}\n{progress_text}",
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton('⛔️ Cancel', callback_data='close')]
                    ]
                )
            )
        except Exception as e:
            print(f"Error editing query: {e}")


def humanbytes(size, convert_to_int=False):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    
    if convert_to_int:
        size = int(size)
    
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]
