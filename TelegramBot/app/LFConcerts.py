import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.get("https://afisha.yandex.ru/moscow/concert")
XPath_search_box = '//*[@id="SearchInputComponent"]'
search_box = browser.find_element(by=By.XPATH, value=XPath_search_box)
search_box.send_keys('Баста')
search_box.send_keys(Keys.RETURN)
time.sleep(15)