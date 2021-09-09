import scrapy
from scrapy.http import HtmlResponse
from spaider_scrapy.items import SpaiderScrapyItem

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F']
    page = 0
    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='product-list catalog__product-list']//a[@class='product-card__name smartLink']/@href").getall()
        if response.status == 200 :                          # and self.page<10
            self.page += 1
            next = f'https://book24.ru/search/page-{self.page}/?q=%D0%BF%D1%81%D0%B8%D1%85%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%8F'
        else:
            next = False
        if next:
            print('next book24', ' ', self.page)
            yield response.follow(next, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.books_to_pars)

    def books_to_pars(self, response: HtmlResponse):
        book_name = str(response.xpath("//h1[@class='product-detail-page__title']/text()").get()).replace('\n', '')
        book_url = response.url
        book_author = str(response.xpath("//div[@class='product-characteristic__item']//a[contains(@href, '/author/')]/text()").get()).replace('\n', '')

        if len(response.xpath("//span[@class='app-price product-sidebar-price__price']")) == 0:
            money = '-'
            main_price = 'Нет в наличии'
            sale_price = '-'
        else:
            try:
                money = str(response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()).split()[1]
            except IndexError:
                money = str(response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()).split()[1]
            if response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get() != None:
                main_price = int(str(response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()).split()[0].replace(',', ''))
                sale_price = int(str(response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()).split()[0].replace(',', ''))
            else:
                main_price = int(str(response.xpath("//span[@class='app-price product-sidebar-price__price']/text()").get()).split()[0].replace(',', ''))
                sale_price = 'not sale'

        item = SpaiderScrapyItem(name=book_name, author=book_author, price=main_price, sale_price=sale_price,
                                     url=book_url, money=money)
        yield item