#https://oauth.vk.com/blank.html#access_token=612dfedf8ce48883901da042335c5d8257f277675614c786178b1e7629657117f0955582e3194d3ff5e10&expires_in=86400&user_id=26253495
# 612dfedf8ce48883901da042335c5d8257f277675614c786178b1e7629657117f0955582e3194d3ff5e10


from pprint import pprint
import requests

url_group = 'https://api.vk.com/method/groups.get?user_id=26253495&v=5.52'
url_name = 'https://api.vk.com/method/users.get?user_id=26253495&v=5.52'
headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
params = {'access_token': '612dfedf8ce48883901da042335c5d8257f277675614c786178b1e7629657117f0955582e3194d3ff5e10'}


responce_name = requests.get(url_name, headers=headers, params=params)
responce_group = requests.get(url_group, headers=headers, params=params)

resp_name = responce_name.json()
resp_group = responce_group.json()
print(f'имя - {resp_name["response"][0]["first_name"]}\nid сообществ - {[i for i in resp_group["response"]["items"]]}\nобщее кол-во - {resp_group["response"]["count"]}')

