import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit
from datetime import datetime


def download_image(url, path):
    """Скачивает изображение по ссылке и сохраняет в указаную папку

    Args:
        url (str): Ссылка на изображение
        path (str): Путь до папке где сохранить изображение
    """
    response = requests.get(url)
    response.raise_for_status()

    with open(path, 'wb') as f:
        f.write(response.content)


def get_file_name_from_url(url):
    """Получает имя файла из url

    Args:
        url (str): Ссылка на файл

    Returns:
        str: Расширение файла
    """
    return os.path.basename(urlsplit(url).path)


def get_extension_from_url(url):
    """Получает расширение файла из url

    Args:
        url (str): Ссылка на файл

    Returns:
        str: Расширение файла
    """
    return os.path.splitext(urlsplit(url).path)[1]


def fetch_nasa_apod_images(token):
    """Загружает картинки через API NASA"""
    payload = {'api_key': token,
               'count': 30}
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params=payload)
    response.raise_for_status()

    for json in response.json():
        url_image = json['url']
        download_image(
            url_image, f'./images/{get_file_name_from_url(json["url"])}')


def fetch_nasa_epic_images(token):
    """Загружает картинки через API NASA"""
    payload = {'api_key': token}

    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural', params=payload)
    response.raise_for_status()

    for json in response.json():
        url_image = fetch_nasa_epic_url_image(token, json)
        download_image(
            url_image, f'./images/{json["image"]}{get_extension_from_url(url_image)}')


def fetch_nasa_epic_url_image(token, response_json):
    """Получает ссылку на изображение

    Args:
        token (str): TOKEN API NASA
        response_json (json): Содержит структуру по картинке

    Returns:
        str: Ссылка на изображение
    """
    date_image = datetime.fromisoformat(response_json['date'])

    return f'https://api.nasa.gov/EPIC/archive/natural/{date_image.strftime("%Y/%m/%d")}/png/{response_json["image"]}.png?api_key={token}'


def fetch_spacex_last_launch():
    """Загружает картинки через API SpaceX"""
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
    token = os.getenv('NASA_TOKEN')

    fetch_spacex_last_launch()
    fetch_nasa_apod_images(token)
    fetch_nasa_epic_images(token)
