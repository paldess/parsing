from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client.books
col = db.book24
col2 = db.labirintru

col.delete_many({})
col2.delete_many({})