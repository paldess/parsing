from lxml import html
import requests
from pprint import pprint
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

pd.options.display.max_columns = None

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
responce = requests.get(url, headers=headers)
dom = html.fromstring(responce.text)


news = dom.xpath("//div[@class='js-module']//li[@class='list__item' ]//@href | //td[@class='daynews__main']//@href | //td[@class='daynews__items']//@href")

data_list = []
for i in news:
    list_ = []
    responce_1 = requests.get(i, headers=headers)
    dom_1 = html.fromstring(responce_1.text)
    list_.append(dom_1.xpath(".//h1[@class='hdr__inner']//text()")[0])
    times = datetime.strptime(dom_1.xpath(".//span[@class='note__text breadcrumbs__text js-ago']//@datetime")[0][:19], "%Y-%m-%dT%H:%M:%S")
    list_.append(f'{times.hour}:{times.minute}-{times.day}/{times.month}/{times.year}')
    list_.append(dom_1.xpath(".//a[@class='link color_gray breadcrumbs__link']//text()")[0])
    list_.append(i)
    data_list.append(list_)

data = pd.DataFrame(data_list, columns=['Новость', 'Дата публикации', 'Источник', 'Ссылка'])
print(data)

bd = MongoClient('localhost', 27017)
data_b = bd.lesson_4
lesson = data_b.lesson_4_collection

lesson.delete_many({})
lesson.insert_many(data.to_dict('records'))

