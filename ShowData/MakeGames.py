import json
import random
from bs4 import BeautifulSoup
import requests

def StrToList(str):
  li = str[1:-1].split(', ')
  return li

with open("game_format_h.txt", 'r') as GameFormat_head:
    gameformat_h = GameFormat_head.read()

with open("game_format_f.txt", 'r') as GameFormat_foot:
    gameformat_f = GameFormat_foot.read()

with open("../PrepareData/Data/ScoreData.json", 'r') as ScoreData_json:
    scoredata = json.load(ScoreData_json)

with open("../PrepareData/Data/AnalyzedWordData_1.json", 'r') as WordData_1:
    worddata_1 = json.load(WordData_1)

with open("../PrepareData/Data/AnalyzedWordData_2.json", 'r') as WordData_2:
    worddata_2 = json.load(WordData_2)

with open("../PrepareData/Data/AnalyzedWordData_3.json", 'r') as WordData_3:
    worddata_3 = json.load(WordData_3)

with open("../PrepareData/Data/AnalyzedWordData_4.json", 'r') as WordData_4:
    worddata_4 = json.load(WordData_4)

with open("../PrepareData/Data/AnalyzedWordData_5.json", 'r') as WordData_5:
    worddata_5 = json.load(WordData_5)

worddata = dict(**worddata_1, **worddata_2, **worddata_3, **worddata_4, **worddata_5)

count = 0

for game in worddata:

    tags = []

    tags.extend(worddata[game]["Opencritic"])
    tags.extend(worddata[game]["Metacritic"])
    tags.extend(worddata[game]["IGN"])

    score = 0
    sumscore = 0
    length = 0

    if ("Opencritic chart" in scoredata[game]):
        if (scoredata[game]["Opencritic chart"] is not None):
            li = StrToList(scoredata[game]["Opencritic chart"])
            length += len(li)

            for s in li:
                if (s is not ''):
                    sumscore += int(s)

    if ("Opencritic review" in scoredata[game]):
        if (scoredata[game]["Opencritic review"] is not None):
            li = StrToList(scoredata[game]["Opencritic review"])
            length += len(li)

            for s in li:
                if (s is not ''):
                    sumscore += int(s)

    if ("Metacritic chart" in scoredata[game]):
        if (scoredata[game]["Metacritic chart"] is not None):
            li = StrToList(scoredata[game]["Metacritic chart"])
            length += len(li)

            for s in li:
                if (s is not ''):
                    sumscore += int(s)

    if ("Metacritic review" in scoredata[game]):
        if (scoredata[game]["Metacritic review"] is not None):
            li = StrToList(scoredata[game]["Metacritic review"])
            length += len(li)

            for s in li:
                if (s is not ''):
                    sumscore += int(s)

    if ("IGN" in scoredata[game]):
        if (scoredata[game]["IGN"] is not None):
            li = StrToList(scoredata[game]["IGN"])
            length += len(li)

            for s in li:
                if (s is not ''):
                    sumscore += int(s)

    if (length is not 0):
        score = int(sumscore / length)

    divtext = ""
    tagdivtext = ""

    for tag in tags:
        tagdivtext += '<a class="gradient-button gradient-button-{num}" href="../Tags/{tag}.html" class="no-uline">{tag}</a>'.format(num=random.randrange(1, 8), tag = tag)

    divtext = '<div class="w-container"><h1 class="heading-2">{game}</h1><h2 class="heading"><span class="text-span">Score : {score} / 100</span></h2><h2 class="heading-3">[Main Tags]</h2><div>{tags}</div></div>'.format(game = game, tags = tagdivtext, score = str(score))

    try:
        with open("Games/{}.html".format(game), 'w', encoding="utf-8") as GameFormat:
            GameFormat.write(gameformat_h + divtext + gameformat_f)
    except OSError:
        print("Ignored")

    print("{} is updated {} / {}".format(game, count, len(worddata)))
    count += 1



