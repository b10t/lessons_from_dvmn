import requests


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
