from pymongo import MongoClient
from pprint import pprint

db = MongoClient('localhost', 27017)
link = db.base.links
mail_2 = db.base.mail_2
# link.delete_many({})
# print([i for i in link.find({})])

pprint(len([i for i in mail_2.find({})]))

mail_2.delete_many({})