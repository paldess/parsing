# вариант 2

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sys
import numpy as np
data_category = 1     # сколько основных категорий просмотреть(молочные продукты, мсные продукты и т.д.)
data = pd.DataFrame(columns=['Основная категория', 'Категория', 'Продукт', 'Общая оценка',
                             'Безопасность', 'Натуральность', 'Пищевая ценность', 'Качество', 'Ссылка'])

url = 'https://roscontrol.com/category/produkti'
headers = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

responce = requests.get(url, headers=headers)
soup = bs(responce.text, 'html.parser')

name_category_soup = soup.find_all('div', attrs='catalog__category-name')
name_category_1 = [i for i in name_category_soup]

link_category_soup = soup.find_all('a', attrs='catalog__category-item util-hover-shadow')

num = 0
links = []
for link in link_category_soup:
    url_1 = url + link['href']
    links.append(url_1)

page_product = int(sys.argv[1]) + 1
x = 0
url_1 = 'https://roscontrol.com'
for i in links:
    if x > data_category:
        break
    name_category_1_data = name_category_1[x].text
    responce = requests.get(i, headers=headers)
    soup = bs(responce.text, 'html.parser')
    name_category_soup = soup.find_all('div', attrs='catalog__category-name')
    name_category = [i.text for i in [i for i in name_category_soup]]
    link = [url_1+q['href'] for q in soup.find_all('a', attrs='catalog__category-item util-hover-shadow')]

    y = 0

    for w in link:
        link_product_1 = []
        if page_product < 2:
            page_product = 2
        for i in range(1, page_product):
            params = {'page': i}
            responce_1 = requests.get(w, headers=headers, params=params)
            soup_1 = bs(responce_1.text, 'html.parser')

            link_product = [url_1+e['href'] for e in soup_1.find_all('a', attrs='block-product-catalog__item js-activate-rate util-hover-shadow clear')]
            for h in link_product:
                link_product_1.append(h)
        for t in link_product_1:
            responce_2 = requests.get(t, headers=headers)
            soup_2 = bs(responce_2.text, 'html.parser')
            name_product = soup_2.find('h1', attrs='main-title testlab-caption-products util-inline-block')
            total = soup_2.find('div', attrs='product__single-rev-total')       # total green
            safety = soup_2.find_all('div', attrs='rate-item group')
            reit = [i.text.replace('\n', '') for i in safety]
            num += 1
            print(num, name_product.text)
            # print(total.text.split()[0])

            try:
                sting = len(data['Категория'])
                data_reit_1 = {'Основная категория': name_category_1_data, 'Категория': name_category[y],
                                                    'Продукт': name_product.text.replace(name_category[y].strip(), ''),
                                                    'Общая оценка': total.text.split()[0], 'Ссылка': t}

                data_reit = {}
                for i in range(len(reit)):
                    cat = reit[i].split()[1]
                    if len(reit[i].split()) == 3:
                        cat = f'{reit[i].split()[1]} {reit[i].split()[2]}'
                    data_reit[cat] = reit[i].split()[0]
                data_reit.update(data_reit_1)
                data.loc[sting] = data_reit

            except AttributeError:
                continue


        y += 1
    x += 1

data.to_csv('data.csv', index=False)
arc = pd.read_csv('data.csv')
print(arc)



