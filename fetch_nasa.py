import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote, urlencode
from datetime import datetime
import time
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


def fetch_nasa_apod_images(token):
    """Загружает картинки через API NASA."""
    payload = {'api_key': token,
               'count': 30}
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params=payload)
    response.raise_for_status()

    for image_json in response.json():
        url_image = image_json['url']

        if urlsplit(url_image).netloc == 'apod.nasa.gov':
            download_image(
                url_image, f'./images/{get_file_name_from_url(image_json["url"])}')


def fetch_nasa_epic_images(token):
    """Загружает картинки через API NASA."""
    payload = {'api_key': token}

    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural', params=payload)
    response.raise_for_status()

    for image_json in response.json():
        url_image = fetch_nasa_epic_url_image(token, image_json)

        if urlsplit(url_image).netloc == 'api.nasa.gov':
            download_image(
                url_image, f'./images/{image_json["image"]}{get_extension_from_url(url_image)}')


def fetch_nasa_epic_url_image(token, image_json):
    """Получает ссылку на изображение.

    Args:
        token (str): TOKEN API NASA
        image_json (json): Метаданные изображения

    Returns:
        str: Ссылка на изображение
    """
    payload = {'api_key': token}
    date_image = datetime.fromisoformat(image_json['date'])

    params = '?%s' % urlencode(payload)

    return f'https://api.nasa.gov/EPIC/archive/natural/{date_image.strftime("%Y/%m/%d")}/png/{image_json["image"]}.png{params}'


if __name__ == '__main__':
    path_to_image = './images/'
    Path(path_to_image).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    timeout = int(os.getenv('TIMEOUT', 86400))

    while True:
        fetch_nasa_apod_images(nasa_token)
        fetch_nasa_epic_images(nasa_token)

        time.sleep(timeout)
