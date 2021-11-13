import os
from pathlib import Path
from dotenv import load_dotenv
import telegram
import random
import time
from fetch_spacex import fetch_spacex_last_launch
from fetch_nasa import fetch_nasa_apod_images, fetch_nasa_epic_images


if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    nasa_token = os.getenv('NASA_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    id_telegram_channel = os.getenv('ID_TELEGRAM_CHANNEL')
    timeout = int(os.getenv('TIMEOUT', 86400))

    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    while True:
        fetch_spacex_last_launch(path_to_images)
        fetch_nasa_apod_images(nasa_token, path_to_images)
        fetch_nasa_epic_images(nasa_token, path_to_images)

        bot = telegram.Bot(token=telegram_token)

        files = os.listdir(path_to_images)

        if files:
            with open(f'{path_to_images}{files[random.randint(0, len(files))]}', 'rb') as photo:
                bot.send_photo(
                    chat_id=id_telegram_channel,
                    photo=photo)

        time.sleep(timeout)
