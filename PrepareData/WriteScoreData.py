import json
import CollectOpencritic as co
import CollectMetacritic as cm

with open("Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

# -------------------------------------------------------------------------------------------------------Initialize Data

dicdata = {}

for game in GameList_data["GameList"]:
    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

# -------------------------------------------------------------------------------------------------------------Edit Data

co.CollectOpencriticScore(dicdata)
cm.CollectMetacriticScore(dicdata)

# ------------------------------------------------------------------------------------------------------------Write Data

with open("Data/ScoreData.json", 'a') as ScoreData:
    ScoreData.write(json.dumps(dicdata))