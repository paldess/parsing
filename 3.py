import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
import pandas as pd

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', None)

client = MongoClient('localhost', 27017)
data = client.products
collections = data.collections
data.collections.delete_many({})




url = 'https://roscontrol.com'
params = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

data_end = pd.DataFrame(columns=['Основная категория', 'Категория', 'Продукт', 'Общая оценка',
                             'Безопасность', 'Натуральность', 'Пищевая ценность', 'Качество', 'Ссылка'])


def catalogs(url_1, cat):
    category_return = {}
    responce = requests.get(url_1, headers=params)
    soup = BeautifulSoup(responce.text, 'html.parser')

    category = [i.text for i in soup.find_all('div', attrs='catalog__category-name')]
    category_link = [i['href'] for i in soup.find_all('a', attrs='catalog__category-item util-hover-shadow')]
    while True:
        tr = []
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
        for i in numbers.split():
            if not i.isdigit():
                tr.append(0)
            elif int(i)>len(category) or int(i)<1:
                tr.append(0)
        if  0 in tr:
            print(f'значения должны быть целыми, в диапазоне от 1 до {len(category)} включительно')
        else:
            break
    numbers = map(int, numbers.split())
    for i in numbers:
        category_return[category[i-1]] = category_link[i-1]
    return category_return


def catalog_products(url_2, cat_1, cat_2):
    responce = requests.get(url+url_2, headers=params)
    soup = BeautifulSoup(responce.text, 'html.parser')
    page = soup.find_all('div', attrs='page-pagination')
    page = [i.text.split() for i in page][0]
    lim = 0
    for i in page:
        try:
            i = int(i)
            if i > lim:
                lim = i
        except ValueError:
            break
    for q in range(lim):
        pages = {'page': q}
        responce = requests.get(url + url_2, headers=params, params=pages)
        soup = BeautifulSoup(responce.text, 'html.parser')
        for i in [i['href'] for i in soup.find_all('a', attrs='block-product-catalog__item js-activate-rate util-hover-shadow clear')]:
            parameters = {}
            link = url+i
            responce_1 = requests.get(link, headers=params)
            soup_1 = BeautifulSoup(responce_1.text, 'html.parser')
            name = [cat_2, cat_1, soup_1.find('h1', attrs='main-title testlab-caption-products util-inline-block').text]
            try:
                total = soup_1.find('div', id='product__single-rev-total').text.split('\n')
                total[1] = int(total[1]) if total[1]!='\xa0' else None
                total_reit = ['Общая оценка', total[1]]
                reit = [i.text.split() for i in soup_1.find_all('div', attrs='rate-item group')]
                for i in reit:
                    if len(i) > 2:
                        i[1] = i[1]+' '+i[2]
                    parameters[i[1]] = int(i[0])
                parameters[total_reit[0]] = total_reit[1]
                parameters['Основная категория'] = name[0]
                parameters['Категория'] = name[1]
                parameters['Продукт'] = name[2]
                parameters['Ссылка'] = link
                data_end.loc[len(data_end['Категория'])] = parameters
                collections.insert_one(parameters)
            except AttributeError:
                prod = {'Основная категория': name[0], 'Категория': name[1], 'Продукт': name[2], 'Ссылка': link}
                data_end.loc[len(data_end['Категория'])] = prod
                collections.insert_one(prod)
            print(f"Parsing {len(data_end['Категория'])} элемента")
    return data_end

category_1 = catalogs(url+'/category/produkti/', 'Продукты')
for i in category_1:
    category_2 = catalogs(url+category_1[i], i)
    for j in category_2:
        catalog_products(category_2[j], j, i)


data_end.to_csv('data_end.csv', index=False)

# a = collections.find({'Общая оценка': {'$gt': 80}})
# for i in a:
#     print(i)


print('The end')