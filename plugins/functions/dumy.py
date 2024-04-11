import time
import random
from pyrogram import Client
from plugins.functions.display_progress import humanbytes

async def edit_progress_message(query, custom_file_name, total_length, downloaded_size, download_speed):
    total_length_str = humanbytes(total_length, convert_to_int=True)
    downloaded_size_str = humanbytes(downloaded_size)
    speed_str = humanbytes(download_speed) + "/s"
    remaining_time = (int(total_length) - downloaded_size) / download_speed
    estimated_time_str = f"{round(remaining_time)} seconds"
    percentage = (downloaded_size / int(total_length)) * 100

    caption = (
        f"Downloading Please Wait ⏳\n\n"
        f"File Name: {custom_file_name}\n"
        f"Total Size: {total_length_str}\n"
        f"Downloaded Size: {downloaded_size_str}\n"
        f"Download Speed: {speed_str}\n"
        f"Estimated Download Time: {estimated_time_str}\n"
        f"Download Percentage: {percentage:.2f}%"
    )

    await query.message.edit_caption(caption)

async def download_progress(query, custom_file_name, total_length):
    downloaded_size = 0
    start_time = time.time()

    while downloaded_size < int(total_length):
        # Simulating fluctuating download speed between 1MB/s to 2MB/s
        download_speed = 1 + random()  # Assuming random() generates a number between 0 and 1
        downloaded_size += download_speed * 5  # Increase download size every 5 seconds
        await edit_progress_message(query, custom_file_name, total_length, downloaded_size, download_speed)
        await asyncio.sleep(5)

    end_time = time.time()
    print("Download completed in", end_time - start_time, "seconds")
    
