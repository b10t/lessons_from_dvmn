import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from fetch_nasa import fetch_nasa_apod_images, fetch_nasa_epic_images
from fetch_spacex import fetch_spacex_last_launch
from send_image_to_telegram import send_image_to_telegram

if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    nasa_token = os.getenv('NASA_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    telegram_channel_id = os.getenv('ID_TELEGRAM_CHANNEL')
    timeout = int(os.getenv('TIMEOUT', 86400))

    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    while True:
        try:
            fetch_spacex_last_launch(path_to_images)
            fetch_nasa_apod_images(nasa_token, path_to_images)
            fetch_nasa_epic_images(nasa_token, path_to_images)
        except requests.exceptions.ConnectionError as ex:
            raise ex

        send_image_to_telegram(path_to_images,
                               telegram_token,
                               telegram_channel_id)

        time.sleep(timeout)
