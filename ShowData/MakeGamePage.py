import json
import random

with open("../PrepareData/Data/GameList.json", 'r') as GameList_json:
    GameList_data = json.load(GameList_json)

divtext = ""

for game in GameList_data["GameList"]:
    divtext += '<a class="gradient-button gradient-button-{num}" href="Games/{game}.html" class="no-uline">{game}</a>'.format(game = game, num = random.randrange(1, 8))

divtext = "<div>" + divtext + "</div>"

with open("game_page_h.txt", 'r') as GamePage_head:
    gamepage_h = GamePage_head.read()

with open("game_page_f.txt", 'r') as GamePage_foot:
    gamepage_f = GamePage_foot.read()

with open("game_page.html", 'w') as GamePage:
    GamePage.write(gamepage_h + divtext + gamepage_f)