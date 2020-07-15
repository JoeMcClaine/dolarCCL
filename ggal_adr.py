import mysql.connector
import configparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


configDB = configparser.ConfigParser()
configDB.read('db.conf')
dataLoginDB=configDB._sections['default']

mydb = mysql.connector.connect(
  host=dataLoginDB['host'],
  user=dataLoginDB['user'],
  passwd=dataLoginDB['passwd'],
  database=dataLoginDB['database']
)

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

print(mydb)
mycursor = mydb.cursor()

while True:
    #Scraping
    req = requests.get("https://www.investing.com/equities/grupo-financiero-galicia-sa-adr", headers=headers)
    now = datetime.now()
    soup = BeautifulSoup(req.text, "lxml")
    price_adr = soup.find("span", {"id": "last_last"}).string
    print('GGAL','-->',price_adr, '(',now,')')

    #Insert DB
    sql = "INSERT INTO ggal_adr(date, price) VALUES (%s, %s)"
    val = (now, float(price_adr))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    time.sleep(10)


