import mysql.connector
import configparser
import time

ticker='GGAL'

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

while(True):
    sql = "SELECT price FROM sys.ggal_byma order by id desc limit 1"
    mycursor.execute(sql)
    price_byma = mycursor.fetchone()[0]
    print(ticker + ' byma: ' + str(price_byma))

    sql = "SELECT price FROM sys.ggal_adr order by id desc limit 1"
    mycursor.execute(sql)
    price_adr = mycursor.fetchone()[0]
    print(ticker + ' adr: ' + str(price_adr))

    ccl = 10*price_byma/price_adr

    print('ccl-------------------: %.2f' % round(ccl,2))
    mydb.commit()
    
    time.sleep(10)