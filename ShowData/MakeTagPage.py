import json
import random

with open("../PrepareData/Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

with open("../PrepareData/Data/AnalyzedWordData", 'r') as WordData_json:
    WordData_data = json.load(WordData_json)

words = []
data = {}

for game in WordData_data:
    words.extend(WordData_data[game]["Opencritic"])
    words.extend(WordData_data[game]["Metacritic"])
    words.extend(WordData_data[game]["IGN"])

wordset = set(words)
words.clear()
words = list(wordset)

divtext = ""

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

    divtext += '<a class="gradient-button gradient-button-{num}" href="Tags/{word}.html" class="no-uline">{word}</a>'.format(num = random.randrange(1, 8), word = word)

divtext = "<div>" + divtext + "</div>"

with open("tag_page_h.txt", 'r') as TagPage_head:
    tagpage_h = TagPage_head.read()

with open("tag_page_f.txt", 'r') as TagPage_foot:
    tagpage_f = TagPage_foot.read()

with open("tag_page.html", 'w') as TagPage:
    TagPage.write(tagpage_h + divtext + tagpage_f)

with open("Word_GameData.json", 'w') as Word_GameData:
    Word_GameData.write(json.dumps(data))

