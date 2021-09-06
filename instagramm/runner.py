from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from instagramm import settings
from instagramm.spiders.insta import InstaSpider



if __name__ == '__main__':
    crauler_settings = Settings()
    crauler_settings.setmodule(settings)
    process = CrawlerProcess(crauler_settings)
    process.crawl(InstaSpider)


    process.start()