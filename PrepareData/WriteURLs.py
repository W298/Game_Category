import json

with open("Data/GameList.json", 'r') as GameList_json:
    gamelist = json.load(GameList_json)

with open("Debug.txt", 'r') as Data:
    data = Data.readlines()

dicdata = {}

for game in gamelist["GameList"]:
    dicdata[game] = {}

for i in data:
    li = i.split(',')
    li2 = []

    for e in li:
        li2.append(e.strip().strip('\n'))

    try:
        if ("Opencritic" in li2):
            dicdata[li2[0]].update({"Opencritic": {"url": ("https://opencritic.com{}".format(li[2][1:-2])),
                                                   "chart": ("https://opencritic.com{}/charts".format(li[2][1:-2])),
                                                   "review": ("https://opencritic.com{}/reviews".format(li[2][1:-2]))}})

            print("{} in Opencritic".format(li2[0]))

    except KeyError:
       print("Ignored")

    try:
        if ("Metacritic" in li2):
            dicdata[li2[0]].update({"Metacritic": {"url": ("https://www.metacritic.com{}".format(li[2][1:-2]))}})
            print("{} in Opencritic".format(li2[0]))
    except KeyError:
        print("Ignored")

    try:
        if ("IGN" in li2):
            dicdata[li2[0]].update({"IGN": {"url": li[2][1:-2]}})
            print("{} in Opencritic".format(li[2]))

    except KeyError:
        print("Ignored")

with open("Data/URL_List.json", 'w') as URLList_json:
    URLList_json.write(json.dumps(dicdata))