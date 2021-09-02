import scrapy
from  leruaru.items import LeruaruItem

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['http://leroymerlin.ru/']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']
        

    def parse(self, response):
        links = response.xpath("//a[@data-qa='product-image']/@href").getall()
        print()
        for link in links:
            yield response.follow(link, callback=self.parse_in)

    def parse_in(self, response):
        url = response.url
        name = response.xpath('//h1/text()').get()
        price = response.xpath("//uc-pdp-price-view[@slot='second-price']/span[@slot='price']/text()").get()
        metric_price_1 = response.xpath("//uc-pdp-price-view[@slot='second-price']/span[@slot='currency']/text()").get()
        metric_price_2 = response.xpath("//uc-pdp-price-view[@slot='second-price']/span[@slot='unit']/text()").get()
        pictures = response.xpath('//picture[@slot="pictures"]/source[1]/@data-origin').getall()
        print()
        yield LeruaruItem(url=url, name=name, price=price, metric_price_1=metric_price_1, metric_price_2=metric_price_2, pictures=pictures)

