import requests
from bs4 import BeautifulSoup
import json

dic_name = {"GameList" : []}
dic_url = {"Opencritic": {}, "IGN": {}, "Metacritic" : {}}

def OpencriticGameList():
    N = 1
    bsobj = []
    Rawdata = []
    names = []
    urls = []

    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)

    for i in range(N):
        bsobj.append(BeautifulSoup(requests.get("https://opencritic.com/browse/pc/all-time/score/" + str(i + 1)).text,
                                   "html.parser"))

    for i in range(N):
        Rawdata.append(bsobj[i].select(Selector_data["opencritic_gamelist"]))

    for li in Rawdata:
        for n in li:
            names.append(n.text)
            urls.append("https://opencritic.com" + n["href"])
            print(n.text + " is found!(Opencritic)")  # Debugging

    dic_name["GameList"].extend(names)

    for i in range(len(names)):
        dic_url["Opencritic"][names[i]] = {"url": urls[i], "chart": (urls[i] + "/charts"),
                                           "review": (urls[i] + "/reviews")}


def IGNGameList():

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)

    bsobj = BeautifulSoup(requests.get("https://www.ign.com/reviews/games", headers=headers).text, "html.parser")
    Rawdata = bsobj.select("#page > div.jsx-3405344643 > main > div.jsx-3448337366.review-content-feed > section.jsx-3995683049.grid.page-content.content-feed-grid > section.jsx-3272103915.main-content > article:nth-child(1) > div > div.jsx-201083914.item-details > a")

    print(Rawdata)

def MetacriticGameList():
    N = 1
    bsobj = []
    Rawdata = []
    names = []
    urls = []

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)

    for i in range(N):
        bsobj.append(BeautifulSoup(requests.get("https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered?sort=desc&page=" + str(i), headers=headers).text,
                                   "html.parser"))
    for i in range(N):
        Rawdata.append(bsobj[i].select(Selector_data["metacritic_gamelist"]))

    for li in Rawdata:
        for n in li:
            names.append(n.text.strip())
            urls.append("https://www.metacritic.com" + n["href"])
            print(n.text.strip() + " is found!(Metacritic)")  # Debugging

    dic_name["GameList"].extend(names)

    for i in range(len(names)):
        dic_url["Metacritic"][names[i]] = {"url": urls[i], "chart": (urls[i] + "/charts"),
                                           "review": (urls[i] + "/reviews")}


def WriteData():
    with open("Data/GameList.json", 'a') as GameList:
        GameList.write(json.dumps(dic_name))

    with open("Data/URL_List.json", 'a') as URLList:
        URLList.write(json.dumps(dic_url))


OpencriticGameList()
MetacriticGameList()
WriteData()