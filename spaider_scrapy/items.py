# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpaiderScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    money = scrapy.Field()

    # print()