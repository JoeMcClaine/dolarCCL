from flask import Flask
from flask_restful import Resource, Api
import mysql.connector
import configparser
from datetime import datetime


app = Flask(__name__)
api = Api(app)


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



class priceGGAL_ADR(Resource):
    def get(self):
        now = datetime.now()
        current_second = str(int(now.strftime("%S"))+1)
        print("Segundo: "+current_second)
        sql="SELECT Price FROM ggal_adr_test where id=%s"
        mycursor = mydb.cursor()
        parm=(current_second,)
        mycursor.execute(sql, parm)

        return str(mycursor.fetchone()[0])

class cclGGAL(Resource):
    def get(self):
        now = datetime.now()
        current_second = str(int(now.strftime("%S"))+1)
        print("Segundo: "+current_second)
        sql="SELECT Price FROM ggal_adr_test where id=%s"
        mycursor = mydb.cursor()
        parm=(current_second,)
        mycursor.execute(sql, parm)
        priceADR = mycursor.fetchone()[0]

        sql="SELECT Price FROM ggal_byma_test where id=%s"
        mycursor.execute(sql, parm)
        priceBYMA = mycursor.fetchone()[0]
        ccl = 10*priceBYMA/priceADR

        return str(ccl)



api.add_resource(priceGGAL_ADR, '/ggal_adr')  # Route_1
api.add_resource(cclGGAL, '/ccl_ggal')  # Route_2


if __name__ == '__main__':
     app.run(port='5000')