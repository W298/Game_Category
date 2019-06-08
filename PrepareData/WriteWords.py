import json
import re

with open("Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

with open("Debug_WordData.txt", 'r') as WordData:
    worddata = WordData.readlines()

dicdata = {}
dicdata2 = {}

for game in GameList_data["GameList"]:
    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

for game in GameList_data["GameList"]:
    dicdata2[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

for str in worddata:
    index_1 = str.find(',')
    index_2 = str.find(',', index_1 + 1)

    game = str[:index_1]
    dis = str[index_1 + 2: index_2]
    listr = str[index_2 + 2: -2]

    listr = re.sub("'", '', listr)

    try:
        if (dis == "Opencritic"):
            dicdata[game].update({"Opencritic": listr})
            print("Updated {}".format(game))
        elif (dis == "Opencritic summary"):
            dicdata2[game].update({"Opencritic": listr})
            print("Updated {}".format(game))
        elif (dis == "Metacritic"):
            dicdata[game].update({"Metacritic": listr})
            print("Updated {}".format(game))
        elif (dis == "IGN"):
            dicdata[game].update({"IGN": listr})
            print("Updated {}".format(game))
        elif (dis == "IGN summary"):
            dicdata2[game].update({"IGN": listr})
            print("Updated {}".format(game))

    except KeyError:
        print("Ignored")

with open("Data/WordData.json", 'w') as WordData_json:
    WordData_json.write(json.dumps(dicdata))