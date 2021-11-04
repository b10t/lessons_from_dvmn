import requests

payload = {"n": "",
           "T": "",
           "q": "",
           "m": "",
           "lang": "ru"}

places = ['Лондон', 'Шереметьево', 'Череповец']

for place in places:
  response = requests.get(f'https://wttr.in/{place}', params=payload)
  response.raise_for_status()

  print(response.text)
