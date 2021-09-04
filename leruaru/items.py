# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeruaruItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    metric_price = scrapy.Field()
    metric_price_2 = scrapy.Field()
    pictures = scrapy.Field()

