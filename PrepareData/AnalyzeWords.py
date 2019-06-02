import requests
from bs4 import BeautifulSoup
import json

with open("Data/SelectorList.json", 'r') as Selector_json:
    Selector_data = json.load(Selector_json)

with open("Data/WordData.json", 'r') as Word_json:
    Word_data = json.load(Word_json)

headers = {'User-Agent': 'Chrome/66.0.3359.181'}

dicdata = {}

for game in Word_data:
    opli = Word_data[game]["Opencritic"]
    meli = Word_data[game]["Metacritic"]
    ignli = Word_data[game]["IGN"]

    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

    if (opli is not None):
        for word in opli:
            html = requests.get("https://dictionary.cambridge.org/dictionary/english/" + word, headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["dict"])

            classif = ""
            for str in Rawdata:
                classif = str.text

            if (classif.strip() == "adjective" or classif.strip() == "adverb"):
                print("{0} is {1}".format(word, classif))
            else:
                print("{0} is removed {1}".format(word, classif))
                opli.remove(word)

        dicdata[game]["Opencritic"].extend(opli)

    if (meli is not None):
        for word in meli:
            html = requests.get("https://dictionary.cambridge.org/dictionary/english/" + word, headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["dict"])

            classif = ""
            for str in Rawdata:
                classif = str.text

            if (classif.strip() == "adjective" or classif.strip() == "adverb"):
                print("{0} is {1}".format(word, classif))
            else:
                print("{0} is removed {1}".format(word, classif))
                meli.remove(word)

        dicdata[game]["Metacritic"].extend(meli)

    if(ignli is not None):
        for word in ignli:
            html = requests.get("https://dictionary.cambridge.org/dictionary/english/" + word, headers=headers).text

            BSObject = BeautifulSoup(html, "html.parser")

            Rawdata = BSObject.select(Selector_data["dict"])

            classif = ""
            for str in Rawdata:
                classif = str.text

                if (classif.strip() == "adjective" or classif.strip() == "adverb"):
                    print("{0} is {1}".format(word, classif))
                else:
                    print("{0} is removed {1}".format(word, classif))
                    ignli.remove(word)

            dicdata[game]["IGN"].extend(ignli)

with open("Data/AnalyzedWordData.json", 'w') as output_json:
    output_json.write(dicdata)