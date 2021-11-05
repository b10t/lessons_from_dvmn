import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BITLY_TOKEN')


def shorten_link(token, url):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': url}

    response = requests.post(
        f'https://api-ssl.bitly.com/v4/bitlinks',
        headers=headers,
        json=payload)

    response.raise_for_status()

    return response.json()['id']


def count_clicks(token, bitLink):
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'units': -1}

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitLink}/clicks/summary',
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
    try:
        user_input = input('Введите ссылку: ')

        if is_bitlink(token, user_input):
            print('Кол-во кликов', count_clicks(token, user_input))
        else:
            bitLink = shorten_link(token, user_input)
            print('Битлинк', bitLink)
    except requests.exceptions.HTTPError:
        print('Error')
