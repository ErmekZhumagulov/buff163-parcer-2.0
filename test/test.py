from bs4 import BeautifulSoup
import urllib.request

html_page = urllib.request.urlopen('https://buff.163.com/market/csgo#tab=selling&page_num=1')
soup = BeautifulSoup(html_page, 'html.parser')
els = soup.find_all("ul", {"class": "card_csgo"})
print(els)
#for el in els:
#    print(el)
