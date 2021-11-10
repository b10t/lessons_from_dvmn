import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import time
from download_and_save_images import download_image


def fetch_spacex_last_launch():
    """Загружает картинки через API SpaceX."""
    response = requests.get('https://api.spacexdata.com/v4/launches')

    for i in response.json():
        if i['links']['flickr']['original']:
            for index, url in enumerate(i['links']['flickr']['original'], 1):
                response = requests.get(url)
                response.raise_for_status()

                download_image(
                    url,
                    './images/spacex%s.jpg' % index)
            break


if __name__ == '__main__':
    path_to_image = './images/'
    Path(path_to_image).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        fetch_spacex_last_launch()

        time.sleep(timeout)
