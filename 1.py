# вариант 2

import requests
from bs4 import BeautifulSoup as bs

url = 'https://roscontrol.com/category/produkti'
headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

responce = requests.get(url, headers=headers)
soup = bs(responce.text, 'html.parser')

name_category_soup = soup.find_all('div', attrs='catalog__category-name')
name_category = [i for i in name_category_soup]

link_category_soup = soup.find_all('a', attrs='catalog__category-item util-hover-shadow')

for link in link_category_soup:
    url_1 = url + link['href']
    print(url_1)


