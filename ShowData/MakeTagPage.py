import json
import random
import re

with open("../PrepareData/Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

with open("../PrepareData/Data/AnalyzedWordData_1.json", 'r') as WordData_json_1:
    WordData_data_1 = json.load(WordData_json_1)

with open("../PrepareData/Data/AnalyzedWordData_2.json", 'r') as WordData_json_2:
    WordData_data_2 = json.load(WordData_json_2)

with open("../PrepareData/Data/AnalyzedWordData_3.json", 'r') as WordData_json_3:
    WordData_data_3 = json.load(WordData_json_3)

with open("../PrepareData/Data/AnalyzedWordData_4.json", 'r') as WordData_json_4:
    WordData_data_4 = json.load(WordData_json_4)

with open("../PrepareData/Data/AnalyzedWordData_5.json", 'r') as WordData_json_5:
    WordData_data_5 = json.load(WordData_json_5)

WordData_data = dict(**WordData_data_1, **WordData_data_2, **WordData_data_3, **WordData_data_4, **WordData_data_5)

words = []
data = {}

for game in WordData_data:
    words.extend(WordData_data[game]["Opencritic"])
    words.extend(WordData_data[game]["Metacritic"])
    words.extend(WordData_data[game]["IGN"])

wordset = set(words)
words.clear()
words = list(wordset)

newwords = []

for word in words:
    newwords.append(re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', word))

divtext = ""

count = 0

for word in newwords:
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

    print("{} is updated {} / {}".format(word, count, len(newwords)))
    count += 1

    divtext += '<a class="gradient-button gradient-button-{num}" href="Tags/{word}.html" class="no-uline">{word}</a>'.format(num = random.randrange(1, 8), word = word)

divtext = "<div>" + divtext + "</div>"

try:
    with open("tag_page_h.txt", 'r') as TagPage_head:
        tagpage_h = TagPage_head.read()

    with open("tag_page_f.txt", 'r') as TagPage_foot:
        tagpage_f = TagPage_foot.read()

    with open("tag_page.html", 'w', encoding="utf-8") as TagPage:
        TagPage.write(tagpage_h + divtext + tagpage_f)

    with open("Word_GameData.json", 'w', encoding="utf-8") as Word_GameData:
        Word_GameData.write(json.dumps(data))

except:
    print("Ignored")

