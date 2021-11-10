import os
from pathlib import Path
from dotenv import load_dotenv
import telegram
import random
import time

if __name__ == '__main__':
    path_to_images = './images/'
    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    id_telegram_channel = os.getenv('ID_TELEGRAM_CHANNEL')
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        bot = telegram.Bot(token=str(telegram_token))

        for root, dirs, files in os.walk(path_to_images):
            with open(f'{path_to_images}{files[random.randint(0, len(files))]}', 'rb') as photo:
                bot.send_photo(
                    chat_id=id_telegram_channel,
                    photo=photo)

        time.sleep(timeout)
