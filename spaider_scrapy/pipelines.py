# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpaiderScrapyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.books

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        dict_item = dict(item)
        if len([i for i in collection.find(dict_item)]) == 0:
            collection.insert_one(dict_item)
        return item
