import scrapy
import re
import json
from urllib.parse import urlencode
from instagramm import options_parser
from scrapy.loader import ItemLoader
from instagramm.items import InstagrammItem


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    reg_url = 'https://www.instagram.com/accounts/login/ajax/'

    user_name = 'desqip'
    user_pass = '#PWD_INSTAGRAM_BROWSER:10:1630833865:AV5QAJM2bG/IoognU1Wwq3LJORHcT13nEGkfSFNsuB33WFViDZhopvay4L3gXAhC/OygqauHEo9/6YfmoccEozTE5Ti5wiCPGYMgFGpQE9xzcrg+tYmcZDRfmCWgX935ZPoKuVbyh1DuuhkX5RQHmA=='

    query = '8c2a529969ee035a5063f2fc8602a0fd'


    def parse(self, response):
        csrf = self.token(response.text)
        yield scrapy.FormRequest(self.reg_url,
                           method='POST',
                           callback=self.login,
                           formdata={'username': self.user_name, 'enc_password': self.user_pass},
                           headers={'x-csrftoken': csrf})

    def login(self, response):
        j_data = response.json()
        x = options_parser.user_find
        if j_data['authenticated']:
            for i in x:
                yield response.follow(f"/{i}", callback=self.read_subscribes, cb_kwargs={'user': i})


    def token(self, text):
        search = re.search('\"csrf_token\":\"\w+\"', text).group()
        return search.split(':')[1].replace('"', '')


# сюда отправляет всех указанных пользователей по очереди в строке 36, но далее обрабатывается лишь последний
    def read_subscribes(self, response, user):
        id = re.search('\"id\":\"\w+\"', response.text).group().split(':')[1].replace('"', '')

        yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id}/followers/?count=12',
                              callback=self.my_subscribe, cb_kwargs={'user': user, 'id_user': id, 'next': 12}, headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id}/following/?count=12',
                              callback=self.subscribs, cb_kwargs={'user': user, 'id_user': id, 'next': 12},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def my_subscribe(self, response, user, id_user, next):
        fr = response.json()
        for i in fr['users']:
            status = 'in'
            main_user = user
            main_id = id_user
            user_name = i['username']
            id = i['pk']
            photo = i['profile_pic_url']
            item = InstagrammItem(status=status, main_user=main_user, main_id=main_id, user_name=user_name, id=id, photo=photo)
            yield item
        if fr['big_list']:
            next += 12
            print(next)
            yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id_user}/followers/?count=12', #&max_id={next}',
                              callback=self.my_subscribe, cb_kwargs={'user': user, 'id_user': id_user, 'next': next},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})


    def subscribs(self, response, user, id_user, next):
        fr = response.json()
        for i in fr['users']:
            status = 'out'
            main_user = user
            main_id = id_user
            user_name = i['username']
            id = i['pk']
            photo = i['profile_pic_url']
            item = InstagrammItem(status=status, main_user=main_user, main_id=main_id, user_name=user_name, id=id, photo=photo)
            yield item
        if fr['big_list']:
            next += 12
            print(next)
            yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id_user}/following/?count=12', #&max_id={next}',
                callback=self.subscribs, cb_kwargs={'user': user, 'id_user': id_user, 'next': next},
                headers={'User-Agent': 'Instagram 155.0.0.37.107'})
