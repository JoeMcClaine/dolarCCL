import mysql.connector
import configparser


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

sql = "show tables"
mycursor.execute(sql)
#mydb.commit()

result = mycursor.fetchall()

for i in range(len(result)):
	print(result[i])
