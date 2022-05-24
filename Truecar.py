from bs4 import BeautifulSoup
import requests
import re
import mysql.connector


user = mysql.connector.connect(user = 'root', password = '', host = '127.0.0.1', database = 'user_detalis')     #khandan jadval car az database karmanadan
user_cursor = user.cursor()


x = str(input("Enter your car company: "))                                                    # khandan va moratab sazi etelaat sait
car = requests.get('https://www.truecar.com/used-cars-for-sale/listings/%s' %(x))
car = BeautifulSoup(car.text, 'html.parser')


agahi = car.findAll('div', attrs={'class' : 'd-flex w-100 justify-content-between'})        #joda va moratab sazi karkard mashin ha
pricelist = []
for i in agahi[:20]:
    price = re.search(r'(?<=</svg>)\d+,+\d+', str(i))
    pricelist.append(price.group(0))


for i in pricelist:                                                                           # rikhtan dar database
    detalis = "INSERT INTO car VALUES (%s)"  # jagozari dar database
    val = (i,)
    user_cursor.execute(detalis, val)
    user.commit()