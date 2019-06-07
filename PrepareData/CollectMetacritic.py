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

    count = 1

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

            try:
                dicdata[game]["Metacritic"].append(int(score))
                print("Metacritic chart page score analyzed: " + game + "{} / {}".format(count, len(
                    GameList_data["GameList"])))  # Debugging

                with open("Debug_ScoreData.txt", 'a') as Data:
                    Data.write("{}, Metacritic chart, {} \n".format(game, score))

            except:
                print("Ignored")

            count += 1

    # ---------------------------------------------------------------------------------------------Get review page score

    count = 1

    for game in GameList_data["GameList"]:
        if("Metacritic" in URL_data[game].keys()):
            html = requests.get(url=((URL_data[game]["Metacritic"]["url"]) + "/critic-reviews"), headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["metacritic_criticpage_score"])

            data = []
            for str in Rawdata:
                score = str.text
                data.append(score)

            try:
                dicdata[game]["Metacritic"].extend(data)

                print("Metacritic review page score analyzed: " + game + "{} / {}".format(count, len(
                    GameList_data["GameList"])))  # Debugging

                with open("Debug_ScoreData.txt", 'a') as Data:
                    Data.write("{}, Metacritic review, {} \n".format(game, data))
            except:
                print("Ignored")

            count += 1


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

