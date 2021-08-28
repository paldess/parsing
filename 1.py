from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from pprint import pprint
from pymongo import MongoClient




db = MongoClient('localhost', 27017)
base = db.base
mail = base.mail

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
links = [i for i in driver.find_elements_by_xpath("//a[contains(@href, '/inbox/0')]")]
links[0].click()


time.sleep(1)
number = 0
while True:
    title = driver.find_element_by_class_name('thread__subject').text
    try:
        new = driver.find_element_by_class_name("mob_font2_mr_css_attr").text
    except NoSuchElementException:
        new = 'Нет содержимого для отображения'
    from_ = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    date = driver.find_element_by_class_name('letter__date').text

    letter = {'date': date, 'from':from_, 'title': title, 'news': new}
    if len([i for i in mail.find(letter)])==0:
        mail.insert_one(letter)
        number += 1
    try:
        driver.find_element_by_xpath("//span[@data-title-shortcut='Ctrl+↓']").click()
        time.sleep(0.8)
    except NoSuchElementException:
        break
print(f'Добавлено {number} сообщ. Всего в базе данных {len([i for i in mail.find({})])}')