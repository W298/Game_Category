import json
import random

with open("game_format_h.txt", 'r') as GameFormat_head:
    gameformat_h = GameFormat_head.read()

with open("game_format_f.txt", 'r') as GameFormat_foot:
    gameformat_f = GameFormat_foot.read()

with open("Word_GameData.json", 'r') as Word_GameData:
    wordgamedata = json.load(Word_GameData)

with open("../PrepareData/Data/ScoreData.json", 'r') as ScoreData_json:
    scoredata = json.load(ScoreData_json)

with open("../PrepareData/Data/URL_List.json", 'r') as URLList_json:
    urllist = json.load(URLList_json)

with open("../PrepareData/Data/AnalyzedWordData.json", 'r') as WordData:
    worddata = json.load(WordData)

for game in worddata:

    tags = []

    tags.extend(game["Opencritic"])

    divtext = '<div class="w-container"><h1 class="heading-2">{game}</h1><h2 class="heading"><span class="text-span">Score : {score} / 10</span></h2><h2 class="heading-3">[Main Tags]</h2><div>{tags}</div><h3 class="heading-4">Game Info.</h3><ul class="list"><li><strong>Avaliable On : </strong></li><li><strong>Developer :</strong></li><li><strong>Publishers : </strong></li><li><strong>Genre :</strong></li></ul></div>'.format(
        game = game, score = scoredata[game], )