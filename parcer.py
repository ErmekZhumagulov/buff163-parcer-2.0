from selenium import webdriver
from selenium.webdriver.common.by import By
from currency_converter import CurrencyConverter
from datetime import datetime
import csv
import os.path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMessageBox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import urllib.request

Form, Window = uic.loadUiType("ui.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
errorWindow = QMessageBox()

def errors(text):
    errorWindow.setWindowTitle('Error')
    errorWindow.setText(text)
    errorWindow.setIcon(QMessageBox.Icon.Warning)
    errorWindow.setStandardButtons(QMessageBox.StandardButton.Ok)
    errorWindow.exec()

    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    path_to_chromedriver = 'chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

    browser.get('https://buff.163.com/market/steam_inventory')
    browser.refresh()

    # delay
    html_page = urllib.request.urlopen('https://google.com')
    soup = BeautifulSoup(html_page, 'html.parser')

converter = CurrencyConverter()

def categoryGroupAll():
    categoryGroup = ''
    pricefrom = form.textEdit_parcingPriceFrom.toPlainText()
    pricetill = form.textEdit_parcingPriceTill.toPlainText()
    pagesToParce = form.textEdit_PagesToParce.toPlainText()

    for j in range(int(pagesToParce), 0, -1):
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "localhost:8989")
        path_to_chromedriver = 'chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

        browser.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(j) + '&category_group=' + categoryGroup + '&min_price=' + str(pricefrom) + '&max_price=' + str(pricetill))
        browser.refresh()

        # delay
        html_page = urllib.request.urlopen('https://google.com')
        soup = BeautifulSoup(html_page, 'html.parser')

        links = []
        for i in range(1, 21):
            try:
                item = browser.find_element(By.CLASS_NAME, 'card_csgo > li:nth-child(' + str(i) + ') > a')
                links.append(item.get_attribute('href'))
            except NoSuchElementException:
                pass

        for i in links:
            browser = webdriver.Chrome(executable_path=path_to_chromedriver)

            browser.get(i)

            itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

            try:
                steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
                steamPriceStrRemoveLastOne = steamPriceStr[:-1]
                steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
                steamPrice = float(steamPriceStrRemoved)

                if steamPrice < 700.00:
                    try:
                        itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
                        itemPriceStrRemoved = itemPriceStr[2:]
                        itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)
                    except ValueError:
                        pass

                    finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)
                    finalPercentageStB = round(((itemPrice - itemPrice / 100 * 2.5) * 100 / steamPrice) - 100, 2)

                    steamPricePrepared = str(steamPrice).replace(".", ",")
                    itemPricePrepared = str(itemPrice).replace(".", ",")
                    finalPercentagePrepared = str(finalPercentage).replace(".", ",")
                    finalPercentageStBPrepared = str(finalPercentageStB).replace(".", ",")

                    timePrepared = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                    file_exists = os.path.isfile('parced-data.csv')

                    with open(r'parced-data.csv', 'a') as file:
                        headers = ['time', 'item', 'steam price, $', 'buff163 price, $', 'b>s income, %', 's>b income, %', 'link']
                        writer = csv.DictWriter(file, delimiter=';', lineterminator='\n', fieldnames=headers)
                        if not file_exists:
                            writer.writeheader()

                        try:
                            file.write(timePrepared + ';' + itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + finalPercentageStBPrepared + ';' + i + '\n')
                        except UnicodeEncodeError:
                            errors('Codec error')
                else:
                    pass
            except NoSuchElementException:
                errors('Element does not exist')

            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        # browser.close()

def categoryGroupStickers():
    categoryGroup = 'sticker'
    pricefrom = form.textEdit_parcingPriceFrom.toPlainText()
    pricetill = form.textEdit_parcingPriceTill.toPlainText()
    pagesToParce = form.textEdit_PagesToParce.toPlainText()

    for j in range(int(pagesToParce), 0, -1):
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "localhost:8989")
        path_to_chromedriver = 'chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

        browser.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(j) + '&category_group=' + categoryGroup + '&min_price=' + str(pricefrom) + '&max_price=' + str(pricetill))
        browser.refresh()

        # delay
        html_page = urllib.request.urlopen('https://google.com')
        soup = BeautifulSoup(html_page, 'html.parser')

        links = []
        for i in range(1, 21):
            try:
                item = browser.find_element(By.CLASS_NAME, 'card_csgo > li:nth-child(' + str(i) + ') > a')
                links.append(item.get_attribute('href'))
            except NoSuchElementException:
                pass

        for i in links:
            browser = webdriver.Chrome(executable_path=path_to_chromedriver)

            browser.get(i)

            itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

            try:
                steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
                steamPriceStrRemoveLastOne = steamPriceStr[:-1]
                steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
                steamPrice = float(steamPriceStrRemoved)

                if steamPrice < 700.00:
                    try:
                        itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
                        itemPriceStrRemoved = itemPriceStr[2:]
                        itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)
                    except ValueError:
                        pass

                    finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)
                    finalPercentageStB = round(((itemPrice - itemPrice / 100 * 2.5) * 100 / steamPrice) - 100, 2)

                    steamPricePrepared = str(steamPrice).replace(".", ",")
                    itemPricePrepared = str(itemPrice).replace(".", ",")
                    finalPercentagePrepared = str(finalPercentage).replace(".", ",")
                    finalPercentageStBPrepared = str(finalPercentageStB).replace(".", ",")

                    timePrepared = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                    file_exists = os.path.isfile('parced-data.csv')

                    with open(r'parced-data.csv', 'a') as file:
                        headers = ['time', 'item', 'steam price, $', 'buff163 price, $', 'b>s income, %', 's>b income, %', 'link']
                        writer = csv.DictWriter(file, delimiter=';', lineterminator='\n', fieldnames=headers)
                        if not file_exists:
                            writer.writeheader()

                        try:
                            file.write(timePrepared + ';' + itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + finalPercentageStBPrepared + ';' + i + '\n')
                        except UnicodeEncodeError:
                            errors('Codec error')
                else:
                    pass
            except NoSuchElementException:
                errors('Element does not exist')

            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        # browser.close()

def categoryGroupOther():
    categoryGroup = 'other'
    pricefrom = form.textEdit_parcingPriceFrom.toPlainText()
    pricetill = form.textEdit_parcingPriceTill.toPlainText()
    pagesToParce = form.textEdit_PagesToParce.toPlainText()

    for j in range(int(pagesToParce), 0, -1):
        opt = Options()
        opt.add_experimental_option("debuggerAddress", "localhost:8989")
        path_to_chromedriver = 'chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

        browser.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(j) + '&category_group=' + categoryGroup + '&min_price=' + str(pricefrom) + '&max_price=' + str(pricetill))
        browser.refresh()

        # delay
        html_page = urllib.request.urlopen('https://google.com')
        soup = BeautifulSoup(html_page, 'html.parser')

        links = []
        for i in range(1, 21):
            try:
                item = browser.find_element(By.CLASS_NAME, 'card_csgo > li:nth-child(' + str(i) + ') > a')
                links.append(item.get_attribute('href'))
            except NoSuchElementException:
                pass

        for i in links:
            browser = webdriver.Chrome(executable_path=path_to_chromedriver)

            browser.get(i)

            itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

            try:
                steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
                steamPriceStrRemoveLastOne = steamPriceStr[:-1]
                steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
                steamPrice = float(steamPriceStrRemoved)

                if steamPrice < 700.00:
                    try:
                        itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
                        itemPriceStrRemoved = itemPriceStr[2:]
                        itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)
                    except ValueError:
                        pass

                    finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)
                    finalPercentageStB = round(((itemPrice - itemPrice / 100 * 2.5) * 100 / steamPrice) - 100, 2)

                    steamPricePrepared = str(steamPrice).replace(".", ",")
                    itemPricePrepared = str(itemPrice).replace(".", ",")
                    finalPercentagePrepared = str(finalPercentage).replace(".", ",")
                    finalPercentageStBPrepared = str(finalPercentageStB).replace(".", ",")

                    timePrepared = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                    file_exists = os.path.isfile('parced-data.csv')

                    with open(r'parced-data.csv', 'a') as file:
                        headers = ['time', 'item', 'steam price, $', 'buff163 price, $', 'b>s income, %', 's>b income, %', 'link']
                        writer = csv.DictWriter(file, delimiter=';', lineterminator='\n', fieldnames=headers)
                        if not file_exists:
                            writer.writeheader()

                        try:
                            file.write(timePrepared + ';' + itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + finalPercentageStBPrepared + ';' + i + '\n')
                        except UnicodeEncodeError:
                            errors('Codec error')
                else:
                    pass
            except NoSuchElementException:
                errors('Element does not exist')

            browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        # browser.close()

def specificLink():
    opt = Options()
    opt.add_experimental_option("debuggerAddress", "localhost:8989")
    path_to_chromedriver = 'chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver, options=opt)

    try:
        browser.get(form.textEdit_link.toPlainText())
        browser.refresh()
    except:
        errors('Wrong link')

    # delay
    html_page = urllib.request.urlopen('https://google.com')
    soup = BeautifulSoup(html_page, 'html.parser')

    links = []
    for i in range(1, 21):
        try:
            item = browser.find_element(By.CLASS_NAME, 'card_csgo > li:nth-child(' + str(i) + ') > a')
            links.append(item.get_attribute('href'))
        except NoSuchElementException:
            pass

    for i in links:
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)

        browser.get(i)

        itemName = browser.find_element(By.CLASS_NAME, 'detail-cont > div:nth-child(1) > h1').text

        try:
            steamPriceStr = browser.find_element(By.CLASS_NAME, 'hide-usd').text
            steamPriceStrRemoveLastOne = steamPriceStr[:-1]
            steamPriceStrRemoved = steamPriceStrRemoveLastOne[3:]
            steamPrice = float(steamPriceStrRemoved)

            if steamPrice < 700.00:
                try:
                    itemPriceStr = browser.find_element(By.CLASS_NAME, 'list_tb_csgo > tr:nth-child(2) > td:nth-child(5)').text
                    itemPriceStrRemoved = itemPriceStr[2:]
                    itemPrice = round(converter.convert(float(itemPriceStrRemoved), 'CNY', 'USD'), 2)
                except ValueError:
                    pass

                finalPercentage = round(((steamPrice - steamPrice / 100 * 15) * 100 / itemPrice) - 100, 2)
                finalPercentageStB = round(((itemPrice - itemPrice / 100 * 2.5) * 100 / steamPrice) - 100, 2)

                steamPricePrepared = str(steamPrice).replace(".", ",")
                itemPricePrepared = str(itemPrice).replace(".", ",")
                finalPercentagePrepared = str(finalPercentage).replace(".", ",")
                finalPercentageStBPrepared = str(finalPercentageStB).replace(".", ",")

                timePrepared = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                file_exists = os.path.isfile('parced-data.csv')

                with open(r'parced-data.csv', 'a') as file:
                    headers = ['time', 'item', 'steam price, $', 'buff163 price, $', 'b>s income, %', 's>b income, %', 'link']
                    writer = csv.DictWriter(file, delimiter=';', lineterminator='\n', fieldnames=headers)
                    if not file_exists:
                        writer.writeheader()

                    try:
                        file.write(timePrepared + ';' + itemName + ';' + steamPricePrepared + ';' + itemPricePrepared + ';' + finalPercentagePrepared + ';' + finalPercentageStBPrepared + ';' + i + '\n')
                    except UnicodeEncodeError:
                        errors('Codec error')
            else:
                pass
        except NoSuchElementException:
            errors('Element does not exist')

        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
    # browser.close()

form.btn_all.clicked.connect(categoryGroupAll)
form.btn_stickers.clicked.connect(categoryGroupStickers)
form.btn_others.clicked.connect(categoryGroupOther)
form.btn_link.clicked.connect(specificLink)

app.exec()
