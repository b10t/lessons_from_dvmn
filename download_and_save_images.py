import requests


def download_image(url, path_to_image, params=None):
    """Скачивает изображение по ссылке и сохраняет в указаную папку.

    Args:
        url (str): Ссылка на изображение
        path_to_image (str): Путь к файлу, в какой необходимо
                             сохранить изображение
        params (dict): Параметры для запроса GET
    """
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(path_to_image, 'wb') as f:
        f.write(response.content)
