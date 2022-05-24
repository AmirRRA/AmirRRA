from bs4 import BeautifulSoup
import requests
import re


divar = requests.get('https://divar.ir/s/fereydunkenar')                                           #khandan site
divar = BeautifulSoup(divar.text,'html.parser')                                                    #moratab sazi
agahi = divar.findAll('div', attrs = {'class' : 'kt-post-card__body'})                             #joda kardan gheymat ha


for i in agahi:
    price = re.search(r'(?<=<div class=\"kt-post-card__description\">)توافقی', str(i))             #joda kardan gheymat hay tavafoghy
    if price:
        title = re.findall(r'(?<=<div class=\"kt-post-card__title\">).+<', str(i))                 #yaftan esm gheymat hai tavafoghy va ejra
        title = title[0]
        title = str(title).split("</")
        title = title[:1]
        print(str(title[0]))