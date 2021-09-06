import scrapy
import re
import json
from urllib.parse import urlencode
from instagramm.options_parser import options_parsing


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']

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
        x = options_parsing()
        if j_data['authenticated']:
            for i in x:
                yield response.follow(f'/{i}', callback=self.read_subscribes, cb_kwargs={'user': i})


    def token(self, text):
        search = re.search('\"csrf_token\":\"\w+\"', text).group()
        return search.split(':')[1].replace('"', '')


        # //div[@class='PZuss']/li//span//@href

    def read_subscribes(self, response, user):
        id = re.search('\"id\":\"\w+\"', response.text).group().split(':')[1].replace('"', '')

        yield response.follow(f'https://i.instagram.com/api/v1/friendships/41812377139/followers/?count=12&search_surface=follow_list_page',
                              callback=self.qwe, cb_kwargs={'user': user, 'id': id}) #, headers={ 'User-Agent' : 'Instagram 155.0.0.37.107'})


    def qwe(self, response, user, id):
        print()