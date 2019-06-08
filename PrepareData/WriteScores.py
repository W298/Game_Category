import json
import re

dicdata = {}

with open("Data/GameList.json", 'r') as GameList_json:
    gamelist = json.load(GameList_json)

with open("Debug_ScoreData.txt", 'r') as Data:
    data = Data.readlines()

for game in gamelist["GameList"]:
    dicdata[game] = {}

for str in data:
    index_1 = str.find(',')
    index_2 = str.find(',', index_1 + 1)

    game = str[:index_1]
    dis = str[index_1 + 2 : index_2]
    listr = str[index_2 + 2 : -2]

    listr = re.sub("'", '', listr)

    try:
        dicdata[game].update({dis: listr})
        print("Updated {}".format(game))
    except KeyError:
        print("Ignored")



with open("Data/ScoreData.json", 'w') as ScoreData_json:
    ScoreData_json.write(json.dumps(dicdata))

