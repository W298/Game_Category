import requests
from bs4 import BeautifulSoup
import json

N = 1
bsobj = []
Rawdata = []
names = []
urls = []

dic_name = {"GameList" : []}
dic_url = {"Opencritic": {}}

for i in range(N):
    bsobj.append(BeautifulSoup(requests.get("https://opencritic.com/browse/pc/all-time/score/" + str(i+1)).text, "html.parser"))

for i in range(N):
    Rawdata.append(bsobj[i].select("body > app-root > div > div > app-browse-platform > div > div.d-flex > div.flex-grow-1 > div.desktop-game-display > div > div > div.game-name.col > a"))

for li in Rawdata:
    for n in li:
        names.append(n.text)
        urls.append("https://opencritic.com" + n["href"])

dic_name["GameList"] = names

for i in range(len(names)):
    dic_url["Opencritic"][names[i]] = {"url": urls[i], "chart": (urls[i] + "/charts"), "review": (urls[i] + "/reviews")}

with open("Data/GameList.json", 'a') as GameList:
    GameList.write(json.dumps(dic_name))

with open("Data/URL_List.json", 'a') as URLList:
    URLList.write(json.dumps(dic_url))

