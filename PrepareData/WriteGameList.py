import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import json

dic_name = {"GameList" : []}
dic_url = {}

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
            print(n.text + " is found!(Opencritic)")  # Debugging

    dic_name["GameList"].extend(names)

    return Rawdata

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

    return Rawdata

def CleanGameList():
    for i in range(len(dic_name["GameList"])):
        for j in range(len(dic_name["GameList"]) - i - 1):
            if(SequenceMatcher(None, dic_name["GameList"][i], dic_name["GameList"][j + i + 1]).ratio() >= 0.95):
                print(dic_name["GameList"][i] + "[" + str(i) + "]" + "\t" + dic_name["GameList"][i + j + 1] + "[" + str(i+j+1) + "]" + " /" + str(SequenceMatcher(None, dic_name["GameList"][i], dic_name["GameList"][j + i + 1]).ratio()))

    tmpli = dic_name["GameList"][:]
    dic_name["GameList"].clear()

    dic_name["GameList"] = list(filter(lambda x: x != "", tmpli))


def InitURLList():
    for ele in dic_name["GameList"]:
        dic_url[ele] = {}

def OpencriticURLList(Rawdata):
    urls = []

    for li in Rawdata:
        for n in li:
            condition = False
            realname = ""

            for j in dic_name["GameList"]:
                if(SequenceMatcher(None, n.text, j).ratio() >= 0.95):
                    realname = j

                    condition = True
                    break

            if (condition):
                urls.append("https://opencritic.com" + n["href"])
                dic_url[realname].update({"Opencritic" : {"url": ("https://opencritic.com" + n["href"]), "chart": ("https://opencritic.com" + n["href"] + "/charts"),
                                           "review": ("https://opencritic.com" + n["href"] + "/reviews")}})

def MetacriticURLList(Rawdata):
    urls = []

    for li in Rawdata:
        for n in li:
            condition = False
            realname = ""

            for j in dic_name["GameList"]:

                if(SequenceMatcher(None, n.text.strip(), j.strip()).ratio() >= 0.95):
                    realname = j.strip()

                    condition = True
                    break

            print(realname, n.text.strip())
            if (condition):
                urls.append("https://www.metacritic.com" + n["href"])
                dic_url[realname].update({"Metacritic" : {"url" : ("https://www.metacritic.com" + n["href"])}})

def WriteData():
    with open("Data/GameList.json", 'a') as GameList:
        GameList.write(json.dumps(dic_name))

    with open("Data/URL_List.json", 'a') as URLList:
        URLList.write(json.dumps(dic_url))



r1 = OpencriticGameList()
r2 = MetacriticGameList()

CleanGameList()
InitURLList()

print(dic_name)

OpencriticURLList(r1)
MetacriticURLList(r2)

print(dic_url)

# def IGNGameList():
#
#     headers = {'User-Agent': 'Chrome/66.0.3359.181'}
#
#     with open("Data/SelectorList.json", 'r') as Selector_json:
#         Selector_data = json.load(Selector_json)
#
#     bsobj = BeautifulSoup(requests.get("https://www.ign.com/reviews/games", headers=headers).text, "html.parser")
#     Rawdata = bsobj.select("#page > div.jsx-3405344643 > main > div.jsx-3448337366.review-content-feed > section.jsx-3995683049.grid.page-content.content-feed-grid > section.jsx-3272103915.main-content > article:nth-child(1) > div > div.jsx-201083914.item-details > a")
#
#     print(Rawdata)