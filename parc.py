from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

path_to_chromedriver = 'D:\work\buff163-parcer-2\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

browser.get("http://www.google.com/")
browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
browser.get('http://stackoverflow.com/')
browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
browser.get('http://yandex.ru/')
browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')

browser.close()
