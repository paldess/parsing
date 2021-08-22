from pymongo import MongoClient
from pprint import pprint

db = MongoClient('localhost', 27017)
a = db.lesson_4.lesson_4_collection.find({})
c = db.lesson_4.lesson_4_new
c.insert_one({'aaa': 12345})


for database in db.list_database_names():
    print({database: [i for i in db[database].list_collection_names()]})
