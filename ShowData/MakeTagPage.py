import json

with open("Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

with open("Data/AnalyzedWordData", 'r') as WordData_json:
    WordData_data = json.load(WordData_json)

words = []
data = {}

for game in WordData_data:
    words.extend(WordData_data[game]["Opencritic"], WordData_data[game]["Metacritic"], WordData_data[game]["IGN"])

wordset = set(words)
words.clear()
words = list(wordset)

for word in words:
    games = []

    for game in WordData_data:
        if (word in WordData_data[game]["Opencritic"]):
            games.append(game)
            break
        elif (word in WordData_data[game]["Metacritic"]):
            games.append(game)
            break
        elif (word in WordData_data[game]["IGN"]):
            games.append(game)
            break

    data.update({word : games})

