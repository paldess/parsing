from pymongo import MongoClient
db = MongoClient('localhost', 27017)
mail = db.base.mail

print([i for i in mail.find({})][-1])

mail.delete_many({'123':'123'})
