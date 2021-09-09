# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstagrammPipeline:
    def __init__(self):
        bd = MongoClient('localhost', 27017)
        self.base = bd.insta


    def process_item(self, item, spider):
        coll = self.base[item['main_user']+'/'+item['main_id']]
        man = dict(item)
        man.pop('main_user')
        man.pop('main_id')
        if len([i for i in coll.find(man)]) == 0:
            coll.insert_one(man)
        return item
