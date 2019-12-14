import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://sites.google.com/site/dailym3uiptv/dl'

res = requests.get(url)
#with open('data.html') as file:
#    res = "".join(file.readlines())

bs = BeautifulSoup(res.text,'html.parser')
trs = bs.find_all('tr', id=lambda x: x and x.startswith('JOT_FILECAB_container_wuid:gx'))

data = {}

for tr in trs:
    ns = tr.find('noscript')
    if ns:
        datetime_obj = datetime.strptime(ns.string,"%b %d, %Y, %I:%M %p")
        a = tr.find('a')['href']
        data[datetime_obj] = 'https://sites.google.com' + a[:-19]

print(max(data.keys()), data[max(data.keys())])

