from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from spaider_scrapy import settings
from spaider_scrapy.spiders.labirintru import LabirintruSpider

if __name__ == '__main__':
    crauler_settings = Settings()
    crauler_settings.setmodule(settings)

    process = CrawlerProcess(crauler_settings)
    process.crawl(LabirintruSpider)

    process.start()