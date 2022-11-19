from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

path_to_chromedriver = 'D:\work\buff163-parcer-2\chromedriver.exe'
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

browser.implicitly_wait(0.5)

browser.get('https://buff.163.com/goods/857571?from=market#tab=selling')

try:
    s = browser.find_element(By.CLASS_NAME, 'hide-usd').text
    print("Element exist - " + s)
except NoSuchElementException:
    print("Element does not exist")

browser.close()
