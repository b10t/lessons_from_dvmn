import os
from pathlib import Path
from dotenv import load_dotenv
import telegram
import random
import time

if __name__ == '__main__':
    path_to_image = './images/'
    Path(path_to_image).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        bot = telegram.Bot(token=str(telegram_token))

        for root, dirs, files in os.walk(path_to_image):
            bot.send_photo(
                chat_id='@photos_from_nasa',
                photo=open(f'{path_to_image}{files[random.randint(0, len(files))]}', 'rb'))

        time.sleep(timeout)
