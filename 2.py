from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from pprint import pprint
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




db = MongoClient('localhost', 27017)
base = db.base
if 'links' in [i for i in db.base.collection_names()]:
    links = base.links
else:
    links = base.links
    links.insert_one({'1':'123'})
    links.delete_many({})
if 'mail_2' in [i for i in db.base.collection_names()]:
    mail_2 = base.mail_2
else:
    mail_2 = base.mail_2
    mail_2.insert_one({'1':'123'})
    mail_2.delete_many({})

chrom = 'D:\chromedriver.exe'
url = 'https://mail.ru/'
driver = webdriver.Chrome(executable_path=chrom)

driver.get(url)


login = driver.find_element_by_xpath("//input[contains(@class, 'email-input')]")
login.send_keys('study.ai_172@mail.ru')
driver.find_element_by_xpath("//button[contains(@class, 'button')]").click()
time.sleep(0.5)
pas = driver.find_element_by_xpath("//input[@type='password']")
pas.send_keys('NextPassword172!!!')
driver.find_element_by_xpath("//button[contains(@class, 'second-button')]").click()

time.sleep(2)
one_link = '0'
while True:
    link = [i for i in driver.find_elements_by_xpath("//a[contains(@href, '/inbox/0')]")]
    for i in link:
        if len([j for j in links.find({'link': i.get_attribute('href')})])==0:
            links.insert_one({'link': i.get_attribute('href')})

    if link[-1]==one_link:
        break
    else:
        one_link = link[-1]
        action = ActionChains(driver)
        body = link[-1]
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

number = 0
links_data = links.find({})
for i in links_data:
    driver.get(i['link'])
    run = 0
    while run == 0:
        try:
            title = driver.find_element_by_class_name('thread__subject').text
            run = 1
        except NoSuchElementException:
            time.sleep(0.1)
    try:
        new = driver.find_element_by_class_name("mob_font2_mr_css_attr").text
    except NoSuchElementException:
        new = 'Нет содержимого для отображения'
    from_ = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    date = driver.find_element_by_class_name('letter__date').text

    letter = {'date': date, 'from': from_, 'title': title, 'news': new}
    if len([i for i in mail_2.find(letter)]) == 0:
        mail_2.insert_one(letter)
        number += 1
links.delete_many({})

print(f'Добавлено {number} сообщ. Всего в базе данных {len([i for i in mail_2.find({})])}')