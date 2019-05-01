import json
import CollectOpencritic as co

with open("Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

# -------------------------------------------------------------------------------------------------------Initialize Data

dicdata = {}

for game in GameList_data["GameList"]:
    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

# -------------------------------------------------------------------------------------------------------------Edit Data

co.CollectOpencriticWords(dicdata)

# ------------------------------------------------------------------------------------------------------------Write Data

with open("Data/WordData.json", 'a') as WordData:
    WordData.write(json.dumps(dicdata))