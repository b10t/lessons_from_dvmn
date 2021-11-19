import os
import time
from datetime import datetime
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv

from download_and_save_images import download_image


def get_file_name_from_url(url):
    """Получает имя файла из url.

    Args:
        url (str): Ссылка на файл

    Returns:
        str: Расширение файла
    """
    return os.path.basename(unquote(urlsplit(url).path))


def get_extension_from_url(url):
    """Получает расширение файла из url.

    Args:
        url (str): Ссылка на файл

    Returns:
        str: Расширение файла
    """
    return os.path.splitext(unquote(urlsplit(url).path))[1]


def fetch_nasa_apod_images(token, path_to_images):
    """Загружает картинки через API NASA."""
    payload = {'api_key': token,
               'count': 3}
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params=payload)
    response.raise_for_status()

    for image_content in response.json():
        image_url = image_content['url']

        if urlsplit(image_url).netloc == 'apod.nasa.gov':
            download_image(
                image_url,
                os.path.join(
                    path_to_images,
                    f'{get_file_name_from_url(image_content["url"])}'))


def fetch_nasa_epic_images(token, path_to_images):
    """Загружает картинки через API NASA."""
    payload = {'api_key': token}

    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural', params=payload)
    response.raise_for_status()

    for image_content in response.json():
        image_url = fetch_nasa_epic_url_image(token, image_content)

        if urlsplit(image_url).netloc == 'api.nasa.gov':
            download_image(
                image_url,
                os.path.join(
                    path_to_images,
                    f'{image_content["image"]}'
                    f'{get_extension_from_url(image_url)}',),
                params={'api_key': token})


def fetch_nasa_epic_url_image(token, image_content):
    """Получает ссылку на изображение.

    Args:
        token (str): TOKEN API NASA
        image_json (json): Метаданные изображения

    Returns:
        str: Ссылка на изображение
    """
    image_date = datetime.fromisoformat(image_content['date'])

    return f'https://api.nasa.gov/EPIC/archive/natural/'\
        f'{image_date.strftime("%Y/%m/%d")}/png/'\
        f'{image_content["image"]}.png'


if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    nasa_token = os.getenv('NASA_TOKEN')
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        fetch_nasa_apod_images(nasa_token, path_to_images)
        fetch_nasa_epic_images(nasa_token, path_to_images)

        time.sleep(timeout)
