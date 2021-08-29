import scrapy
from scrapy.http import HtmlResponse
from spaider_scrapy.items import SpaiderScrapyItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        next = response.xpath("//div[@class='pagination-next']//@href").get()
        if next:
            # print('next')
            yield response.follow(next, callback=self.parse)


        for link in links:
            yield response.follow(link, callback=self.books_to_pars)

    def books_to_pars(self, response: HtmlResponse):
        book_name = response.xpath('//h1/text()').get()
        book_url = response.url
        money = response.xpath("//span[@class='buying-pricenew-val-currency']/text()").get()
        book_author = response.xpath("//a[@data-event-label='author']/text()").get()
        if response.xpath("//span[@class='buying-priceold-val-number']/text()").get() == None:
            main_price = str(response.xpath("//span[@class='buying-price-val-number']/text()").get()) + ' ' + money
        else:
            main_price = str(response.xpath("//span[@class='buying-priceold-val-number']/text()").get()) + ' ' + money
        sale_price = str(response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()) + ' ' + money
        item = SpaiderScrapyItem(name=book_name, author=book_author, price=main_price, sale_price=sale_price, url=book_url)
        yield item