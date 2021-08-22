from pymongo import MongoClient
from pprint import pprint
db = MongoClient('localhost', 27017)
data = db.products
# data.collections.delete_many({})

# x = data.collections.find({'Общая оценка': {'$gt': 80}, 'Качество': {'$gt': 80}})
# pprint([(i, j) for i, j in enumerate(x)])


a = 80
pprint([(i, j) for i, j in enumerate(data.collections.find({'Общая оценка': {'$gt': a}, 'Качество': {'$gt': a}}))])



# a = collections.find({'Общая оценка': {'$gt': 80}})
# for i in a:
#     print(i)