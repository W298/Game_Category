import requests
from bs4 import BeautifulSoup
import json

def CollectIGNScore(dicdata):
    with open("Data/GameList.json", 'r') as GameList_json:
        GameList_data = json.load(GameList_json)
    with open("Data/SelectorList.json", 'r') as Selector_json:
        Selector_data = json.load(Selector_json)
    with open("Data/URL_List.json", 'r') as URL_json:
        URL_data = json.load(URL_json)

    headers = {'User-Agent': 'Chrome/66.0.3359.181'}