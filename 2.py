import requests
from pymongo import MongoClient
from pprint import pprint

w = 'https://roscontrol.com/category/produkti/molochnie_produkti/moloko/'
params = {'page': 2}
responce = requests.get(w, params=params)

# print(responce.url)

client = MongoClient('localhost', 27017)
db = client.people

collection = db.test_collection

# collection.insert_one({'qqq': 15})


collection.delete_one({'qwer': 25})
a = [i for i in collection.find({})]
pprint(a)