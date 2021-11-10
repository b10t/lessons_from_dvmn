import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit
from datetime import datetime
import telegram
import random
import time
from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_apod_images, fetch_nasa_epic_images


if __name__ == '__main__':
    path_to_image = './images/'
    Path(path_to_image).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    id_telegram_channel = os.getenv('ID_TELEGRAM_CHANNEL')
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        fetch_spacex_last_launch()
        fetch_nasa_apod_images(nasa_token)
        fetch_nasa_epic_images(nasa_token)

        bot = telegram.Bot(token=str(telegram_token))

        for root, dirs, files in os.walk(path_to_image):
            bot.send_photo(
                chat_id=id_telegram_channel,
                photo=open(f'{path_to_image}{files[random.randint(0, len(files))]}', 'rb'))

        time.sleep(timeout)
