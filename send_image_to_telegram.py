import os
from pathlib import Path
from dotenv import load_dotenv
import telegram
import random
import time

if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    telegram_channel_id = os.getenv('ID_TELEGRAM_CHANNEL')
    timeout = int(os.getenv('TIMEOUT', 86400))

    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    while True:
        bot = telegram.Bot(token=telegram_token)

        files = os.listdir(path_to_images)

        if files:
            with open(f'{path_to_images}{files[random.randint(0, len(files))]}', 'rb') as photo:
                bot.send_photo(
                    chat_id=telegram_channel_id,
                    photo=photo)

        time.sleep(timeout)
