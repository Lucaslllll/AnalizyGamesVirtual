# from bs4 import BeautifulSoup

# import requests

# html = requests.get("https://www.bet365.com/#/AVR/B146/R^1/").content

# soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())



# from soccerapi.api import Api888Sport
# from soccerapi.api import ApiUnibet
from soccerapi.api import ApiBet365

api = ApiBet365()
url = 'https://www.bet365.com/#/HO/'
odds = api.odds(url)

print(odds)