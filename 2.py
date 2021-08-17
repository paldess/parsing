import requests

w = 'https://roscontrol.com/category/produkti/molochnie_produkti/moloko/'
params = {'page': 2}
responce = requests.get(w, params=params)

print(responce.url)