import os
import requests
from pathlib import Path
from dotenv import load_dotenv


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


def fetch_spacex_last_launch(path_to_image):

    response = requests.get('https://api.spacexdata.com/v4/launches')

    for i in response.json():
        if i['links']['flickr']['original']:
            for index, url in enumerate(i['links']['flickr']['original'], 1):
                download_image(
                    url,
                    path_to_image + 'spacex%s.jpg' % index)


if __name__ == '__main__':
    path_to_image = './images/'
    Path(path_to_image).mkdir(parents=True, exist_ok=True)

    load_dotenv()
    token = os.getenv('BITLY_TOKEN')


    fetch_spacex_last_launch(path_to_image)

    # iFw1FfAz1N5bYdQxHYyZFMzCICyQe3Pjcc7NqEji
