import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import json

dic_name = {"GameList" : []}
dic_url = {}

def OpencriticGameList():
    N = 62
    bsobj = []
    Rawdata = []
    names = []

    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)

    for i in range(N):
        bsobj.append(BeautifulSoup(requests.get("https://opencritic.com/browse/pc/all-time/score/" + str(i + 1)).text,
                                   "html.parser"))
        print(str(i) + " page is prepared")

    for i in range(N):
        Rawdata.append(bsobj[i].select(Selector_data["opencritic_gamelist"]))

    for li in Rawdata:
        for n in li:
            names.append(n.text)
            print(n.text + " is found!(Opencritic)")  # Debugging

    dic_name["GameList"].extend(names)

    return Rawdata

def MetacriticGameList():
    N = 42
    bsobj = []
    Rawdata = []
    names = []

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)

    for i in range(N):
        bsobj.append(BeautifulSoup(requests.get("https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered?sort=desc&page=" + str(i), headers=headers).text,
                                   "html.parser"))
        print(str(i) + " page is prepared")

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
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)

    for ele in GameList_data["GameList"]:
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
                try:
                    dic_url[realname].update({"Opencritic": {"url": ("https://opencritic.com" + n["href"]), "chart": (
                                "https://opencritic.com" + n["href"] + "/charts"),
                                                             "review": ("https://opencritic.com" + n[
                                                                 "href"] + "/reviews")}})

                    with open("Debug.txt", 'a') as Debug:  # Debugging.
                        Debug.write("{game}, Opencritic, {url} \n".format(game=realname, url=n["href"]))
                    break
                except KeyError:
                    break

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

def OpencriticURLListSearchByGameList():

    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)


    count = 0
    for game in GameList_data["GameList"]:
        url = "https://www.google.com/search?q= " + game + " opencritic"
        bsobj = BeautifulSoup(requests.get(url, headers = {'User-Agent': 'Chrome/66.0.3359.181'}).text, "html.parser")

        print("Opencritic / {} ... {}/{}".format(game, count, len(GameList_data["GameList"])))

        Rawdata = bsobj.select("h3>r")

        print(Rawdata)

        tempurl = ""

        for e in Rawdata:
            tempurl = e["href"]

        count += 1



def MetacriticURLListSearchByGameList():

    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)


    count = 0
    for game in GameList_data["GameList"]:
        url = "https://www.metacritic.com/search/game/" + game + "/results?plats[3]=1&search_type=advanced"
        bsobj = BeautifulSoup(requests.get(url, headers = {'User-Agent': 'Chrome/66.0.3359.181'}).text, "html.parser")

        print("Metacritic / {} ... {}/{}".format(game, count, len(GameList_data["GameList"])))

        Rawdata = bsobj.select("#main_content > div.fxdrow.search_results_wrapper > div.module.search_results.fxdcol.gu6 > div.body > ul > li.result.first_result > div > div.basic_stats.has_thumbnail > div > h3 > a")

        tempurl = ""

        for e in Rawdata:
            tempurl = e["href"]

        dic_url[game].update({"Metacritic" : {"url" : "https://www.metacritic.com" + tempurl}})

        with open("Debug.txt", 'a') as Debug: # Debugging.
            Debug.write("{game}, Metacritic, {url} \n".format(game = game, url = tempurl))

        count += 1


def IGNURLList():
    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    with open("Data/GameList.json", 'r')as GameList_json:
        GameList_data = json.load(GameList_json)


    count = 0
    for game in GameList_data["GameList"]:
        bsobj = BeautifulSoup(requests.get("https://www.ign.com/search?q=" + game, headers=headers).text, "html.parser")

        print("IGN / {} ... {}/{}".format(game, count, len(GameList_data["GameList"])))

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

        with open("Debug.txt", 'a') as Debug: # Debugging.
            Debug.write("{game}, IGN, {url} \n".format(game = game, url = url))

        count += 1


def WriteGameList():
    with open("Data/GameList.json", 'a') as GameList:
        GameList.write(json.dumps(dic_name))


def WriteURLList():
    with open("Data/URL_List.json", 'a') as URLList:
        URLList.write(json.dumps(dic_url))



# r1 = OpencriticGameList()
# r2 = MetacriticGameList()
# CleanGameList()
# WriteGameList()

InitURLList()
# OpencriticURLList(r1)
# OpencriticURLListSearchByGameList()
# MetacriticURLListSearchByGameList()
IGNURLList()
# WriteURLList()