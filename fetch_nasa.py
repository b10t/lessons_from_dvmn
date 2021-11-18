import os
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlencode, urlsplit

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

    for image_json in response.json():
        image_url = image_json['url']

        if urlsplit(image_url).netloc == 'apod.nasa.gov':
            download_image(
                image_url,
                os.path.join(
                    path_to_images,
                    f'{get_file_name_from_url(image_json["url"])}'))


def fetch_nasa_epic_images(token, path_to_images):
    """Загружает картинки через API NASA."""
    payload = {'api_key': token}

    try:
        response = requests.get(
            'https://api.nasa.gov/EPIC/api/natural', params=payload)
    except requests.exceptions.ConnectionError as ex:
        raise ex

    response.raise_for_status

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(response.status_code)

    for image_content in response.json():
        url_image = fetch_nasa_epic_url_image(token, image_content)

        if urlsplit(url_image).netloc == 'api.nasa.gov':
            download_image(
                url_image,
                os.path.join(
                    path_to_images,
                    f'{image_content["image"]}{get_extension_from_url(url_image)}'))


def fetch_nasa_epic_url_image(token, image_content):
    """Получает ссылку на изображение.

    Args:
        token (str): TOKEN API NASA
        image_json (json): Метаданные изображения

    Returns:
        str: Ссылка на изображение
    """
    payload = {'api_key': token}
    image_date = datetime.fromisoformat(image_content['date'])

    params = '?%s' % urlencode(payload)

    return f'https://api.nasa.gov/EPIC/archive/natural/{image_date.strftime("%Y/%m/%d")}/png/{image_content["image"]}.png{params}'


if __name__ == '__main__':
    load_dotenv()
    path_to_images = os.getenv('PATH_TO_IMAGES', './images/')
    nasa_token = os.getenv('NASA_TOKEN')
    timeout = int(os.getenv('TIMEOUT', 86400))

    Path(path_to_images).mkdir(parents=True, exist_ok=True)

    while True:
        fetch_nasa_apod_images(nasa_token, path_to_images)
        fetch_nasa_epic_images(nasa_token, path_to_images)

        time.sleep(timeout)
