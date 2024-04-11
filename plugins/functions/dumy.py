import time
import random
import asyncio
from pyrogram import Client
from plugins.functions.display_progress import humanbytes, TimeFormatter


async def edit_progress_message(query, custom_file_name, total_length, downloaded_size, download_speed):
    total_length_str = humanbytes(total_length, convert_to_int=True)
    downloaded_size_str = humanbytes(downloaded_size)
    if downloaded_size >= total_length:  # Prevent size from exceeding total size
        downloaded_size = total_length
    speed_str = "0 B/s" if downloaded_size >= total_length else humanbytes(download_speed * (1024 * 1024)) + "/s"  # Set speed to 0 B/s after 100%
    
    if downloaded_size >= total_length:
        estimated_time_str = "0s"  # Show 0s after 100%
    else:
        remaining_time = (int(total_length) - downloaded_size) / (download_speed * (1024 * 1024))
        estimated_time_str = TimeFormatter(remaining_time * 1000)
    
    percentage = (downloaded_size / int(total_length)) * 100
    if percentage > 100:
        percentage = 100

    caption = (
        f"Downloading Please Wait ⏳\n\n"
        f"File Name: {custom_file_name}\n"
        f"Total Size: {total_length_str}\n"
        f"Size: {downloaded_size_str}\n"
        f"Speed: {speed_str}\n"
        f"ETA: {estimated_time_str}\n"
        f"Percentage: {percentage:.2f}%"
    )

    await query.message.edit_caption(caption)


async def download_progress(query, custom_file_name, total_length):
    downloaded_size_mb = 0  # Initialize Size in MB
    total_length_mb = int(total_length) / (1024 * 1024)  # Convert total length to MB
    start_time = time.time()

    while downloaded_size_mb < total_length_mb:
        # Simulating fluctuating Speed between 1MB/s to 2MB/s
        download_speed_mb = 1 + random.random()  # Speed fluctuates around 1MB/s
        downloaded_size_mb += download_speed_mb * 5  # Increase download size every 5 seconds
        await edit_progress_message(query, custom_file_name, total_length, downloaded_size_mb * (1024 * 1024), download_speed_mb)  # Convert back to bytes
        await asyncio.sleep(5)

    end_time = time.time()
    print("Download completed in", end_time - start_time, "seconds")
    
