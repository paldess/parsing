import requests
import json

name = 'paldess'
url = f'https://api.github.com/users/{name}/repos'

response = requests.get(url)
repos = [i['name'] for i in response.json()]
print(response.status_code)
print(repos)

# with open(f'repositories_{name}', 'w', encoding='UTF-8') as f:
#     f.write(json.dumps(f'{name}:{repos}', ensure_ascii=False))

