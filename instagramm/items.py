# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class InstagrammItem(scrapy.Item):
    # define the fields for your item here like:
    status = scrapy.Field()
    main_user = scrapy.Field()
    main_id = scrapy.Field()
    user_name = scrapy.Field()
    id = scrapy.Field()
    photo = scrapy.Field()
