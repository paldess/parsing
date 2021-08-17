# вариант 2

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

data = pd.DataFrame(columns=['Основная категория', 'Категория', 'Продукт', 'Общая оценка', 'Безопасность', 'Натуральность', 'Пищевая ценность', 'Качество', 'Ссылка'])

url = 'https://roscontrol.com/category/produkti'
headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

responce = requests.get(url, headers=headers)
soup = bs(responce.text, 'html.parser')

name_category_soup = soup.find_all('div', attrs='catalog__category-name')
name_category_1 = [i for i in name_category_soup]

link_category_soup = soup.find_all('a', attrs='catalog__category-item util-hover-shadow')

links = []
for link in link_category_soup:
    url_1 = url + link['href']
    links.append(url_1)


x = 0
for i in links:
    if x > 1:
        break
    name_category_1_data = name_category_1[x].text
    responce = requests.get(i, headers=headers)
    soup = bs(responce.text, 'html.parser')
    name_category_soup = soup.find_all('div', attrs='catalog__category-name')
    name_category = [i.text for i in [i for i in name_category_soup]]
    link = [url+q['href'] for q in soup.find_all('a', attrs='catalog__category-item util-hover-shadow')]

    y = 0
    url_1 = 'https://roscontrol.com'
    for w in link:
        responce_1 = requests.get(w, headers=headers)
        soup_1 = bs(responce_1.text, 'html.parser')

        link_product = [url_1+e['href'] for e in soup_1.find_all('a', attrs='block-product-catalog__item js-activate-rate util-hover-shadow clear')]

        for t in link_product:
            responce_2 = requests.get(t, headers=headers)
            soup_2 = bs(responce_2.text, 'html.parser')
            name_product = soup_2.find('h1', attrs='main-title testlab-caption-products util-inline-block')
            total = soup_2.find('div', attrs='total green')
            safety = soup_2.find_all('div', attrs='rate-item__value')
            reit = [i.text.replace('\n', '') for i in safety]

            try:
                data.loc[len(data['Категория'])] = (name_category_1_data, name_category[y],
                                                    name_product.text.replace(name_category[y].strip(), ''),
                                                    total.text, reit[0], reit[1], reit[2], reit[3], t)
            except AttributeError:
                continue

        y += 1
    x += 1

data.to_csv('data.csv', index=False)
arc = pd.read_csv('data.csv')
print(arc)