from bs4 import BeautifulSoup
import re
from sklearn import tree
import mysql.connector
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver



driver = webdriver.Chrome(ChromeDriverManager().install())                                                              # nasb deriver chrom
driver.get('https://kilid.com/buy/tehran?locations=c_2301021576&subType=buy&type=listing&sort=date,DESC')               #khandan



last_height = driver.execute_script("return document.body.scrollHeight")                                                #scroll kardan ta paian safhe
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(3)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



site = driver.page_source                                                                                               #khandan sorce site va filter
driver.quit()
site = BeautifulSoup(site, 'html.parser')



hoom_price = []                                                                                                         #joda sazi adad daghig geymat be miliard va kalame توافقی
for i in site.findAll('span',attrs={'class':'ng-star-inserted'}):
    price = re.search(r'(?<=">)(.+)<', str(i))
    if str(price.group(1)) != '+':
        price = price.group(1)
        price = price.split()
        if len(price) != 2:
            hoom_price.append(price[0])
        else:
            hoom_price.append(price[1])

detalis = site.findAll('div',attrs={'class':'flex-row al-center jus-center single-info'})                               #joda sazi adad daghigh tedad otagh
room_number = []
metraj = []
for i in range(0,len(detalis)):
    if i == 0 or (i % 3) == 0:
        room = re.search(r'(?<=">)(.+)<', str(detalis[i]))
        room = room.group(1)
        room = room.split()
        room = room[0]
        room_number.append(room)

    elif i == 1 or (i % 3) == 1:                                                                                        #joda sazi adad daghigh metraj
        m = re.search(r'(?<=\"\">)\d*', str(detalis[i]))
        metraj.append(m.group(0))



source = mysql.connector.connect(user = 'root', password = '', host = '127.0.0.1', database = 'home')                   #baz kardan database
source_cursor = source.cursor()



for i in range(0, len(metraj)):                                                                                         #rikhtan dar database
    if hoom_price[i] != 'توافقی':
        database_input = 'INSERT INTO detalis VALUES (%s, %s, %s)'
        valu = (metraj[i], room_number[i], hoom_price[i])
        source_cursor.execute(database_input, valu)
source.commit()



source_cursor.execute('SELECT * FROM detalis')                                                                          #khandan az database
read = source_cursor.fetchall()
x = []
y = []
for i in read:
    x.append([i[0], i[1]])
    y.append(i[2])



clf = tree.DecisionTreeClassifier()                                                                                     #dadan etelaat nemoone be mashin
clf = clf.fit(x, y)



again = 'Yes'
while again == 'Yes':                                                                                                   #takhmin gheymat
    a = int(input('Enter the area of your house in numbers: '))
    b = int(input('Enter the number of rooms in your home: '))
    new_data = [[a, b]]
    answer = clf.predict(new_data)
    print('The price of your house is', answer[0], 'bilion')
    again = str(input('You want to do it again (yes or no) ?!'))
    again = again.strip()
    again = again.capitalize()