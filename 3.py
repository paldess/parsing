import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import mongo_client
import pandas as pd

url = 'https://roscontrol.com'
params = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

data_end = pd.DataFrame()
parameters = []

def catalogs(url_1, cat):
    category_return = {}
    responce = requests.get(url_1, headers=params)
    soup = BeautifulSoup(responce.text, 'html.parser')

    category = [i.text for i in soup.find_all('div', attrs='catalog__category-name')]
    category_link = [i['href'] for i in soup.find_all('a', attrs='catalog__category-item util-hover-shadow')]
    x = 0
    for i in category:
        x += 1
        if x % 4 != 0:
            print(f'-*- {x}-{i}', end=' -*- ')
        else:
            print(f'-*- {x}-{i} -*-')
    numbers = input(f'\n----------Введите каталоги для статистики через пробел из каталога {cat}----------\n')
    if len(numbers) == 0:
        numbers = '1'
    numbers = map(int, numbers.split())

    for i in numbers:
        category_return[category[i-1]] = category_link[i-1]
    return category_return


def catalog_products(url_2):
    responce = requests.get(url_2, headers=params)
    soup = BeautifulSoup(responce.text, 'html.parser')
    for i in [i['href'] for i in soup.find_all('a', attrs='block-product-catalog__item js-activate-rate util-hover-shadow clear')]:
        responce_1 = requests.get(url+i, headers=params)
        soup_1 = BeautifulSoup(responce_1.text, 'html.parser')
        name = soup_1.find('h1', attrs='main-title testlab-caption-products util-inline-block').text
        total = soup_1.find('div', id='product__single-rev-total').text.split('\n')
        total_reit = [total[2], total[1]]
        reit = [i.text.split() for i in soup_1.find_all('div', attrs='rate-item__title')]
        reit_number = [i.text.split('\n') for i in soup_1.find_all('div', attrs='rate-item__value')]
        for i in range(len(reit)):
            if len(reit[i]) > 1:
                reit[i]= reit[i][0] +' ' + reit[i][1]
            else:
                reit[i] = reit[i][0]
        for i in range(len(reit_number)):
            reit_number[i]= reit_number[i][1]

        print(name, total_reit, reit, reit_number)
    # return parameters

category_1 = catalogs(url+'/category/produkti/', 'Продукты')
for i in category_1:
    category_2 = catalogs(url+category_1[i], i)
    for j in category_2:
        data = catalog_products(url+category_2[j])
        # print(data)