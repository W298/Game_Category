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
            print(n.text.strip() + " is found!(Metacritic)")  # Debugging

    dic_name["GameList"].extend(names)

    return Rawdata

def CleanGameList():
    for i in range(len(dic_name["GameList"])):
        for j in range(len(dic_name["GameList"]) - i - 1):
            if(SequenceMatcher(None, dic_name["GameList"][i], dic_name["GameList"][j + i + 1]).ratio() >= 0.95):
                print(dic_name["GameList"][i] + "[" + str(i) + "]" + "\t" + dic_name["GameList"][i + j + 1] + "[" + str(i+j+1) + "]" + " /" + str(SequenceMatcher(None, dic_name["GameList"][i], dic_name["GameList"][j + i + 1]).ratio()))
                dic_name["GameList"][j + i + 1] = ""

    tmpli = dic_name["GameList"][:]
    dic_name["GameList"].clear()

    dic_name["GameList"] = list(filter(lambda x: x != "", tmpli))


def InitURLList():
    for ele in dic_name["GameList"]:
        dic_url[ele] = {}

def OpencriticURLList(Rawdata):

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
                dic_url[realname].update({"Opencritic" : {"url": ("https://opencritic.com" + n["href"]), "chart": ("https://opencritic.com" + n["href"] + "/charts"),
                                           "review": ("https://opencritic.com" + n["href"] + "/reviews")}})

def MetacriticURLList(Rawdata):
    for li in Rawdata:
        for n in li:
            condition = False
            realname = ""

            for j in dic_name["GameList"]:

                if(SequenceMatcher(None, n.text.strip(), j.strip()).ratio() >= 0.95):
                    realname = j.strip()

                    condition = True
                    break

            if (condition):
                dic_url[realname].update({"Metacritic" : {"url" : ("https://www.metacritic.com" + n["href"])}})


def IGNURLList():
    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    urls = []

    for game in dic_name["GameList"]:
        bsobj = BeautifulSoup(requests.get("https://www.ign.com/search?q=" + game, headers=headers).text, "html.parser")

        num = 1

        for i in range(10):
            Rawdata = bsobj.select("#search-list > div:nth-child({0}) > div > div.search-item-sub-title".format(i+1))

            for e in Rawdata:
                det = e.text

            if ("IGN" in det):
                num = i + 1
                break

        Rawdata = bsobj.select("#search-list > div:nth-child({0}) > div > div.search-item-title > a".format(num))

        url = ""

        for e in Rawdata:
            url = e["href"]

        dic_url[game].update({"IGN" : {"url" : url}})

        print("URL of " + game + " is found!") # Debugging


def WriteGameList():
    with open("Data/GameList.json", 'a') as GameList:
        GameList.write(json.dumps(dic_name))


def WriteURLList():
    with open("Data/URL_List.json", 'a') as URLList:
        URLList.write(json.dumps(dic_url))



r1 = OpencriticGameList()
r2 = MetacriticGameList()
CleanGameList()
WriteGameList()

InitURLList()
IGNURLList()
OpencriticURLList(r1)
MetacriticURLList(r2)
WriteURLList()