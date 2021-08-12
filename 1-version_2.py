from pprint import pprint

import requests
user = 's-t-e-v-e-n-k'
url = f'https://api.github.com/users/{user}/repos'
headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}


responce = requests.get(url, headers=headers)

# resp = responce.json()
# print([i['name'] for i in resp])

resp = responce.json()
pprint([resp[i].get('name') for i in range(len(resp))])