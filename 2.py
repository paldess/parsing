from pymongo import MongoClient
from pprint import pprint
db = MongoClient('localhost', 27017)
data = db.products
# data.collections.delete_many({})
x = data.collections.find({})
pprint([(i, j) for i, j in enumerate(x)])