from selenium import webdriver
from selenium.webdriver.common.by import By
from currency_converter import CurrencyConverter
from datetime import date, datetime
import csv
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QWidget, QTextEdit
import time
from selenium.webdriver.common.keys import Keys

Form, Window = uic.loadUiType("untitled.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
errorWindow = QMessageBox()

converter = CurrencyConverter()

def pushed():
    path_to_chromedriver = 'D:\work\buff163-parcer-main-2\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)

    browser.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + form.textEdit.toPlainText())

    links = []
    for i in range(1, 21):
        item = browser.find_element(By.CLASS_NAME, 'market-card > div > ul > li:nth-child(' + str(i) + ') > h3 > a')
        links.append(item.get_attribute('href'))
    browser.close()

    for i in links:
        path_to_chromedriver = 'D:\work\buff163-parcer-main-2\chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)

        browser.get(i)

        itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

        steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
        steamPriceStrRemoveLastOne = steamPriceStr[:-1]
        steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
        steamPrice = float(steamPriceStrRemoved)

        itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
        itemPriceStrRemoved = itemPriceStr[2:]
        itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)

        finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)

        steamPricePrepared = str(steamPrice).replace(".", ",")
        itemPricePrepared = str(itemPrice).replace(".", ",")
        finalPercentagePrepared = str(finalPercentage).replace(".", ",")

        with open(r'oxis.csv', 'a') as file:
            file.write(
                itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + i + '\n')

        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')

form.pushButton.clicked.connect(pushed)

app.exec()