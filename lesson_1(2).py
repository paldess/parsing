import requests

url = "https://api.nasa.gov/planetary/apod?"

headers = {
    'api_key': '7JYhoOfKy7c5YBoux8bdv2dLa4uhTJFwJPpN6Z0m'}

response = requests.get(url, params=headers)

status = response.status_code

with open('ответ сервера.txt', 'w', encoding='UTF-8') as f:
    f.write(f'страница nasa.gov, ответ сервера:\n {status}')


