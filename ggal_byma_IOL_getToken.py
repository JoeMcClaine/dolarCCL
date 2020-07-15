import urllib.request
import json
import requests
import configparser

configIOL = configparser.ConfigParser()
configIOL.read('iol_api.conf')
dataConfig=configIOL._sections['default']

payload = 'username='+dataConfig['username']+'&password='+dataConfig['password']+'&grant_type=password'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

raw_data = requests.request("POST", dataConfig['token_url'], headers=headers, data = payload)
print(raw_data.text.encode('utf8'))
print("----Token----")

jdata = json.loads(raw_data.text.encode('utf8'))
print(jdata["access_token"])

#Token to file
token_file = open("iolApiToken.txt", "w")
n = token_file.write(jdata["access_token"])
token_file.close()
