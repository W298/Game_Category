import requests
from bs4 import BeautifulSoup
import json

def CollectMetacriticScore(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    # ----------------------------------------------------------------------------------------------Get chart page score

    for game in GameList_data["GameList"]:
        if("Metacritic" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["Metacritic"]["url"], headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["metacritic_summarypage_score"])

            score = ""
            for str in Rawdata:
                score = str.text

            if (not score):
                Rawdata = BSObject.select(Selector_data["metacritic_summarypage_score_alter"])

                for str in Rawdata:
                    score = str.text

            dicdata[game]["Metacritic"].append(int(score))
            print("Metacritic Summary page score analyzed: " + game)  # Debugging

    # ---------------------------------------------------------------------------------------------Get review page score

    for game in GameList_data["GameList"]:
        if("Metacritic" in URL_data[game].keys()):
            html = requests.get(url=((URL_data[game]["Metacritic"]["url"]) + "/critic-reviews"), headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["metacritic_criticpage_score"])

            data = []
            for str in Rawdata:
                score = str.text
                data.append(score)

            dicdata[game]["Metacritic"].extend(data)
            print("Metacritic Summary page score analyzed: " + game)  # Debugging


def CollectMetacriticWords(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}

    for game in GameList_data["GameList"]:
        if ("Metacritic" in URL_data[game].keys()):
            html = requests.get(url=((URL_data[game]["Metacritic"]["url"]) + "/critic-reviews"), headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["metacritic_criticpage_word"])

            if not Rawdata:
                Rawdata = BSObject.select(Selector_data["metacritic_criticpage_word_alter"])

            words = []

            try:
                for li in Rawdata:
                    for cont in li:
                        if (cont):
                            words.extend(cont.strip().split())

                dicdata[game]["Metacritic"].extend(words)
                print("Metacritic critic page words collected: " + game)

            except TypeError:
                print(game + " is ignored")

