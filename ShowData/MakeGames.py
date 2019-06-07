import json
import random
from bs4 import BeautifulSoup
import requests

with open("game_format_h.txt", 'r') as GameFormat_head:
    gameformat_h = GameFormat_head.read()

with open("game_format_f.txt", 'r') as GameFormat_foot:
    gameformat_f = GameFormat_foot.read()

with open("../PrepareData/Data/ScoreData.json", 'r') as ScoreData_json:
    scoredata = json.load(ScoreData_json)

with open("../PrepareData/Data/AnalyzedWordData.json", 'r') as WordData:
    worddata = json.load(WordData)

for game in worddata:

    tags = []

    tags.extend(worddata[game]["Opencritic"])
    tags.extend(worddata[game]["Metacritic"])
    tags.extend(worddata[game]["IGN"])

    score = 0
    sumscore = 0

    for s in scoredata[game]["Opencritic"]:
        sumscore += s

    for s in scoredata[game]["Metacritic"]:
        sumscore += s

    for s in scoredata[game]["IGN"]:
        sumscore += s

    score = (sumscore) / (len(scoredata[game]["Opencritic"]) + len(scoredata[game]["Metacritic"]) + len(scoredata[game]["IGN"]))

    divtext = ""
    tagdivtext = ""

    for tag in tags:
        tagdivtext += '<a class="gradient-button gradient-button-{num}" href="Tags/{tag}.html" class="no-uline">{tag}</a>'.format(num=random.randrange(1, 8), tag = tag)

    divtext = '<div class="w-container"><h1 class="heading-2">{game}</h1><h2 class="heading"><span class="text-span">Score : {score} / 10</span></h2><h2 class="heading-3">[Main Tags]</h2><div>{tags}</div></div>'.format(game = game, tags = tagdivtext, score = str(score))

    with open("Games/{}.html".format(game), 'w') as GameFormat:
        GameFormat.write(gameformat_h + divtext + gameformat_f)



