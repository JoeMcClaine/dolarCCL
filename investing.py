import requests
from bs4 import BeautifulSoup
import configparser
from datetime import datetime

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

config = configparser.ConfigParser()
config.read('tickerSource.conf')
tickers=config._sections['default'].items()
for ticker, link in tickers:
    req = requests.get(link, headers=headers)
    now = datetime.now()
    soup = BeautifulSoup(req.text, "lxml")
    #print(soup.title.string)
    #<span class="arial_26 inlineblock pid-32371-last" id="last_last" dir="ltr">9.85</span>
    print(ticker,'-->',soup.find("span", {"id": "last_last"}).string, '(',now,')')

