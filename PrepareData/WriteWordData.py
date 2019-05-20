import json
import CollectOpencritic as co
import CollectMetacritic as cm

with open("Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

# -------------------------------------------------------------------------------------------------------Initialize Data

dicdata = {}
dicdata2 = {}

for game in GameList_data["GameList"]:
    dicdata[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

for game in GameList_data["GameList"]:
    dicdata2[game] = {"Opencritic": [], "Metacritic": [], "IGN": []}

# -------------------------------------------------------------------------------------------------------------Edit Data

co.CollectOpencriticWords(dicdata)
co.CollectOpencriticSummaryWords(dicdata2)
cm.CollectMetacriticWords(dicdata)

# ------------------------------------------------------------------------------------------------------------Write Data

with open("Data/WordData.json", 'a') as WordData:
    WordData.write(json.dumps(dicdata))

with open("Data/SummaryData.json", 'a') as SummaryData:
    SummaryData.write(json.dumps(dicdata2))