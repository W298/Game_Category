import requests
from bs4 import BeautifulSoup
import json

def CollectIGNScore(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    count = 1

    for game in GameList_data["GameList"]:
        if("IGN" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["IGN"]["url"], headers=headers).text
            BSObject = BeautifulSoup(html, "html.parser")
            Rawdata = BSObject.select(Selector_data["ign_score"])

            score = 0
            for ele in Rawdata:
                score = ele.text

            try:
                dicdata[game]["IGN"].append(score)

                print("IGN score analyzed: " + game + "{} / {}".format(count, len(
                    GameList_data["GameList"])))  # Debugging

                with open("Debug_ScoreData.txt", 'a') as Data:
                    Data.write("{}, IGN, {} \n".format(game, score))

            except:
                print("Ignored")

            count += 1


def CollectIGNWords(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    for game in GameList_data["GameList"]:
        if("IGN" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["IGN"]["url"], headers=headers).text
            BSObject = BeautifulSoup(html, "html.parser")
            Rawdata = BSObject.select("#article-content")

            data = []

            for p in Rawdata:
                str = p.text.replace('\n', "").replace(" " * 44, "").replace(" " * 20, "").replace("Share.", "").replace('.', "")
                data.append(str.split())

            dicdata[game]["IGN"].extend(data)


def CollectIGNSummaryWords(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    for game in GameList_data["GameList"]:
        if ("IGN" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["IGN"]["url"], headers=headers).text
            BSObject = BeautifulSoup(html, "html.parser")
            Rawdata = BSObject.select(Selector_data["ign_summarypage_score"])

            data = []

            for div in Rawdata:
                for el in div:
                    data.append(el)

        dicdata[game]["IGN"].extend(data)