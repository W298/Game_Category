import requests
from bs4 import BeautifulSoup
import json

def CollectOpencriticScore(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    # ----------------------------------------------------------------------------------------------Get chart page score

    for game in GameList_data["GameList"]:
        html = requests.get(url=URL_data[game]["chart"]).text

        BSObject = BeautifulSoup(html, "html.parser")

        Rawdata = BSObject.select(Selector_data["opencritic_chartpage_score"])
        data = []
        for str in Rawdata:
            score = str.text

            if (score and score[0] == " "):
                indexofslice = score.find('/')
                if (indexofslice == -1):
                    data.append(int(score[1:-1]))
                else:
                    firstdigit = score[1:indexofslice - 1]
                    seconddigit = score[indexofslice + 2:]
                    data.append(int((float(firstdigit) / float(seconddigit)) * 100))

        dicdata[game]["Opencritic"].extend(data)

    # ---------------------------------------------------------------------------------------------Get review page score

    for game in GameList_data["GameList"]:
        html = requests.get(url=URL_data[game]["review"]).text

        BSObject = BeautifulSoup(html, "html.parser")

        Rawdata = BSObject.select(Selector_data["opencritic_reviewpage_score"])
        data = []
        for str in Rawdata:
            score = str.text

            if (score and not score == "Unscored" and score.find('/') != -1):
                indexofslice = score.find('/')
                firstdigit = score[1:indexofslice - 1]
                seconddigit = score[indexofslice + 2:]
                data.append(int((float(firstdigit) / float(seconddigit)) * 100))

        dicdata[game]["Opencritic"].extend(data)