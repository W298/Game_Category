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
        if("Opencritic" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["Opencritic"]["chart"]).text

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
            print("Opencritic chart page score analyzed: " + game)  # Debugging

    # ---------------------------------------------------------------------------------------------Get review page score

    for game in GameList_data["GameList"]:
        if ("Opencritic" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["Opencritic"]["review"]).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["opencritic_reviewpage_score"])
            data = []
            for str in Rawdata:
                score = str.text

                if (score and not score is "Unscored" and '/' in score):
                    indexofslice = score.find('/')
                    firstdigit = score[1:indexofslice - 1]
                    seconddigit = score[indexofslice + 2:]
                    if (firstdigit.isdigit() and seconddigit.isdigit()):
                        data.append(int((float(firstdigit) / float(seconddigit)) * 100))

            dicdata[game]["Opencritic"].extend(data)
            print("Opencritic reivew page score analyzed: " + game)  # Debugging

def CollectOpencriticWords(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)


    for game in GameList_data["GameList"]:
        if ("Opencritic" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["Opencritic"]["url"]).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["opencritic_infopage_words"])

            if not Rawdata:
                Rawdata = BSObject.select(Selector_data["opencritic_infopage_words_alter"])

                if not Rawdata:
                    Rawdata = BSObject.select(Selector_data["opencritic_infopage_words_alter2"])

                    if not Rawdata:
                        Rawdata = BSObject.select(Selector_data["opencritic_infopage_words_alter3"])

            for str in Rawdata:
                text = str.text

            txli = text.split()

            dicdata[game]["Opencritic"].extend(txli)
            print("Opencritic info page words collected: " + game)

def CollectOpencriticSummaryWords(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    for game in GameList_data["GameList"]:
        if ("Opencritic" in URL_data[game].keys()):
            html = requests.get(url=URL_data[game]["Opencritic"]["url"]).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdatali = []

            Rawdatali.append(BSObject.select(Selector_data["opencritic_summarypage_words_1"]))
            Rawdatali.append(BSObject.select(Selector_data["opencritic_summarypage_words_2"]))
            Rawdatali.append(BSObject.select(Selector_data["opencritic_summarypage_words_3"]))

            textli = []

            for Raw in Rawdatali:
                for str in Raw:
                    textli.append(str.text.strip())

            if (textli is not None):
                dicdata[game]["Opencritic"].extend(textli)

            print("Opencritic summary page words collected: " + game)