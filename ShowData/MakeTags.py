import json
import random

with open("Word_GameData.json", 'r') as Word_GameData:
    Data = json.load(Word_GameData)

with open("tag_page_h.txt", 'r') as TagPage_head:
    tagpage_h = TagPage_head.read()

with open("tag_page_f.txt", 'r') as TagPage_foot:
    tagpage_f = TagPage_foot.read()

for word in Data:

    divtext = ""

    for game in Data[word]:
        divtext += '<a class="gradient-button gradient-button-{num}" href="../Games/{game}.html" class="no-uline">{game}</a>'.format(num=random.randrange(1, 8), game=game)

    divtext = "<div>" + divtext + "</div>"

    try:
        with open("Tags/{}.html".format(word), 'w', encoding="utf-8") as TagPage:
            TagPage.write(tagpage_h + divtext + tagpage_f)
    except FileNotFoundError:
        print("Ignored")