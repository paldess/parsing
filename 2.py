from pymongo import MongoClient
from pprint import pprint

db = MongoClient('localhost', 27017)
a = db.lesson_4.lesson_4_yandex_news.find({'Источник': 'Lenta.ru'})
pprint([(i, j) for i, j in enumerate(a, 1)])
for database in db.list_database_names():
    print({database: [i for i in db[database].list_collection_names()]})
