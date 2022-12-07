from selenium import webdriver
from selenium.webdriver.common.by import By
from currency_converter import CurrencyConverter
from datetime import date, datetime
import csv
import os.path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget, QTextEdit
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request

converter = CurrencyConverter()

# you can edit these next 3 row code
pricefrom = 1
priceto = 4
for j in range(1, 5):
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    path_to_chromedriver = 'D:\work\buff163-parcer-2\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

    browser.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(j) + '&category_group=sticker&min_price=' + str(pricefrom) + '&max_price='  + str(priceto))

    browser.refresh()

    # delay
    html_page = urllib.request.urlopen('https://google.com')
    soup = BeautifulSoup(html_page, 'html.parser')

    links = []
    for i in range(1, 21):
        item = browser.find_element(By.CLASS_NAME, 'card_csgo > li:nth-child(' + str(i) + ') > a')
        links.append(item.get_attribute('href'))

    for i in links:
        browser = webdriver.Chrome(executable_path = path_to_chromedriver)

        browser.get(i)

        itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

        try:
            steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
            steamPriceStrRemoveLastOne = steamPriceStr[:-1]
            steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
            steamPrice = float(steamPriceStrRemoved)

            if steamPrice < 700.00:
                itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
                itemPriceStrRemoved = itemPriceStr[2:]
                itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)

                finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)
                finalPercentageStB = round(((itemPrice - itemPrice / 100 * 2.5) * 100 / steamPrice) - 100, 2)

                steamPricePrepared = str(steamPrice).replace(".", ",")
                itemPricePrepared = str(itemPrice).replace(".", ",")
                finalPercentagePrepared = str(finalPercentage).replace(".", ",")
                finalPercentageStBPrepared = str(finalPercentageStB).replace(".", ",")

                timePrepared = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                file_exists = os.path.isfile('oxis.csv')

                with open(r'oxis.csv', 'a') as file:
                    headers = ['time', 'item', 'steam price, $', 'buff163 price, $', 'b>s income, %', 's>b income, %', 'link']
                    writer = csv.DictWriter(file, delimiter=';', lineterminator='\n', fieldnames=headers)
                    if not file_exists:
                        writer.writeheader()

                    try:
                        file.write(timePrepared + ';' + itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + finalPercentageStBPrepared + ';' + i + '\n')
                    except UnicodeEncodeError:
                        print('codec error')
            else:
                pass
        except NoSuchElementException:
            print('Element does not exist')

        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')

    browser.close()
