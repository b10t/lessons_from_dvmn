import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

token = os.getenv('BITLY_TOKEN')


def shorten_link(token, url):
    """Сокращяет ссылку через интерфейс bit.ly

    Args:
        token (str): TOKEN API Bitly
        url (str): Ссылка

    Returns:
        str: Сокращённая ссылка
    """
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': url}

    response = requests.post(
        f'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=payload)

    response.raise_for_status()

    return response.json()['link']


def count_clicks(token, bitly_link):
    """Возвращает количество кликов по ссылке

    Args:
        token (str): TOKEN API Bitly
        bitly_link (str): Сокращённая ссылка

    Returns:
        int: Количество кликов по ссылке
    """
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'units': -1}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitly_link}/clicks/summary',
        headers=headers,
        params=payload)

    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token, url):
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers=headers)

    return response.ok


if __name__ == '__main__':
    url = urlparse(input('Введите ссылку: '))

    if url.scheme:
        url_without_schema = url.netloc + url.path

        if is_bitlink(token, url_without_schema):
            try:
                print('Кол-во кликов',
                      count_clicks(token, url_without_schema))
            except requests.exceptions.HTTPError:
                print('Ошибка при получении количества кликов.')
        else:
            try:
                print('Битлинк', shorten_link(token, url.geturl()))
            except:
                print('Ошибка при получении короткой ссылки.')
    else:
        print('Введите ссылку полность, со схемой (http://... или https://...)')
