import requests

url = "https://api.nasa.gov/planetary/apod?"

headers = {
    'api_key': '7JYhoOfKy7c5YBoux8bdv2dLa4uhTJFwJPpN6Z0m'}

response = requests.get(url, params=headers)

print(response.status_code)