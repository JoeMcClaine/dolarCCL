import urllib.request
import json
import requests
import configparser
import time
from datetime import datetime
import mysql.connector
import os

#get token
os.system("py ggal_byma_IOL_getToken.py")
#open token
token_file = open("iolApiToken.txt", "r")
token = token_file.read()
token_file.close()
token_refresh = 60

configIOL = configparser.ConfigParser()
configIOL.read('iol_api.conf')
dataConfig=configIOL._sections['default']
urlAndToken = dataConfig['ggal_url']+token

configDB = configparser.ConfigParser()
configDB.read('db.conf')
dataLoginDB=configDB._sections['default']

mydb = mysql.connector.connect(
  host=dataLoginDB['host'],
  user=dataLoginDB['user'],
  passwd=dataLoginDB['passwd'],
  database=dataLoginDB['database']
)
print(mydb)
mycursor = mydb.cursor()

payload = {}
headers = {
  'Authorization': 'Bearer '
}

while(True):
    if(token_refresh<=0):
        #refresca token
        os.system("py ggal_byma_IOL_getToken.py")
        token_refresh=60

    headers.update(Authorization = 'Bearer '+token)
    raw_data = requests.request("GET", urlAndToken, headers=headers, data = payload)
    now = datetime.now()
    jdata = json.loads(raw_data.text.encode('utf8'))
    #print("GGAL precio actual: "+str(jdata["ultimoPrecio"]))
    price = jdata["ultimoPrecio"]
    print("GGAL MERVAL: " + str(price))
    #Insert DB
    sql = "INSERT INTO ggal_byma(date, price) VALUES (%s, %s)"
    val = (now, float(price))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    time.sleep(10)
    token_refresh-=1
