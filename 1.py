from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint

chrom = 'D:\chromedriver.exe'
url = 'https://mail.ru/'
driver = webdriver.Chrome(executable_path=chrom)

driver.get(url)


login = driver.find_element_by_xpath("//input[contains(@class, 'email-input')]")
login.send_keys('study.ai_172@mail.ru')
driver.find_element_by_xpath("//button[contains(@class, 'button')]").click()
time.sleep(2)
pas = driver.find_element_by_xpath("//input[@type='password']")
pas.send_keys('NextPassword172!!!')
driver.find_element_by_xpath("//button[contains(@class, 'second-button')]").click()


time.sleep(5)
links = driver.find_elements_by_tag_name('a')
pprint([i.get_attribute('href') for i in links])


# for i in links:
#     driver_1 = webdriver.Chrome(executable_path=chrom)
#     driver_1.
print()