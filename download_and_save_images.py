import requests


def download_image(url, path_to_image):
    """Скачивает изображение по ссылке и сохраняет в указаную папку.

    Args:
        url (str): Ссылка на изображение
        path_to_image (str): Путь к файлу, в какой необходимо сохранить изображение
    """
    response = requests.get(url)
    response.raise_for_status()

    with open(path_to_image, 'wb') as f:
        f.write(response.content)