import requests
from bs4 import BeautifulSoup

html = requests.get(url="https://opencritic.com/game/7513/world-war-z/charts").text

BSObject = BeautifulSoup(html, "html.parser")

print(BSObject.select("body > app-root > div > div > app-game-data-visualizations > div > div.d-flex.mb-4 > div.flex-grow-1 > div > app-game-data-visualization-bar-row > div.chart-row-v2 > div > div.d-flex.review-header-info.mt-2 > span.mr-2 > app-score-display > span"))

# CSS Selector를 이용하여 BeautifulSoup의 Select로 해당되는 모든 값을 가져옴