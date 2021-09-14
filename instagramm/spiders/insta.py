import scrapy
import re
from scrapy.http import HtmlResponse
from urllib.parse import urlencode
from instagramm import options_parser
from instagramm.items import InstagrammItem
from copy import deepcopy


class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    reg_url = 'https://www.instagram.com/accounts/login/ajax/'

    user_name = 'desqip'
    user_pass = '#PWD_INSTAGRAM_BROWSER:10:1630833865:AV5QAJM2bG/IoognU1Wwq3LJORHcT13nEGkfSFNsuB33WFViDZhopvay4L3gXAhC/OygqauHEo9/6YfmoccEozTE5Ti5wiCPGYMgFGpQE9xzcrg+tYmcZDRfmCWgX935ZPoKuVbyh1DuuhkX5RQHmA=='

    query = '8c2a529969ee035a5063f2fc8602a0fd'
    headers = {'User-Agent': 'Instagram 155.0.0.37.107'}
    api_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response:HtmlResponse):
        csrf = self.token(response.text)
        yield scrapy.FormRequest(self.reg_url,
                           method='POST',
                           callback=self.login,
                           formdata={'username': self.user_name, 'enc_password': self.user_pass},
                           headers={'x-csrftoken': csrf})

    def login(self, response:HtmlResponse):
        j_data = response.json()
        x = options_parser.user_find
        if j_data['authenticated']:
            for i in x:
                yield response.follow(f"/{i}", callback=self.read_subscribes, cb_kwargs={'user': deepcopy(i)})


    def token(self, text):
        search = re.search('\"csrf_token\":\"\w+\"', text).group()
        return search.split(':')[1].replace('"', '')


# сюда отправляет всех указанных пользователей по очереди в строке 36, но далее обрабатывается лишь последний
    def read_subscribes(self, response:HtmlResponse, user):
        id = re.search('\"id\":\"\w+\"', response.text).group().split(':')[1].replace('"', '')

        yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id}/followers/?count=12',
                              callback=self.my_subscribe, cb_kwargs={'user': deepcopy(user), 'id_user': deepcopy(id)}, headers=self.headers)

        # yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id}/following/?count=12&max_id=12',
        #                       callback=self.subscribs, cb_kwargs={'user': user, 'id_user': id, 'next': 0},
        #                       headers=self.headers)

    # def my_subscribe(self, response:HtmlResponse, user, id_user):
    #     fr = response.json()
    #     if fr['big_list'] == True:
    #         next = fr['next_max_id']
    #         url_follow = f'{self.api_url}{id_user}/followers/?count=12&max_id={next}'
    #         yield response.follow(url_follow,
    #                               callback=self.my_subscribe, cb_kwargs={'user': user, 'id_user': id_user},
    #                               headers=self.headers)
    def my_subscribe(self, response: HtmlResponse, user, id_user):
        J_data = response.json()
        if J_data['next_max_id']:
            next = J_data['next_max_id']
            url_follow = f'{self.api_url}{id_user}/followers/?count=12&max_id={next}'
            yield response.follow(url_follow,
                                  callback=self.my_subscribe,
                                  cb_kwargs={'user': user,
                                             'id_user': id_user},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        for i in J_data['users']:
            status = 'in'
            main_user = user
            main_id = id_user
            user_name = i['username']
            id = i['pk']
            photo = i['profile_pic_url']
            item = InstagrammItem(status=status, main_user=main_user, main_id=main_id, user_name=user_name, id=id, photo=photo)
            yield item



    # def subscribs(self, response, user, id_user, next):
    #     fr = response.json()
    #     for i in fr['users']:
    #         status = 'out'
    #         main_user = user
    #         main_id = id_user
    #         user_name = i['username']
    #         id = i['pk']
    #         photo = i['profile_pic_url']
    #         item = InstagrammItem(status=status, main_user=main_user, main_id=main_id, user_name=user_name, id=id, photo=photo)
    #         yield item
    #     if fr['big_list']:
    #         next += 12
    #         print(next)
    #         yield response.follow(f'https://i.instagram.com/api/v1/friendships/{id_user}/following/?count=12#&max_id={next}',
    #             callback=self.subscribs, cb_kwargs={'user': user, 'id_user': id_user, 'next': next},
    #             headers=self.headers)
