## primeira forma

#from bs4 import BeautifulSoup

#import requests

#html = requests.get("https://www.bet365.com/#/AVR/B146/R^1/").content

#soup = BeautifulSoup(html, 'html.parser')

#print(soup.prettify())


## segunda forma

# from soccerapi.api import Api888Sport
# from soccerapi.api import ApiUnibet
#from soccerapi.api import ApiBet365

#api = ApiBet365()
#url = 'https://www.bet365.com/#/HO/'
#odds = api.odds(url)

#print(odds)


## outra forma


from bs4 import BeautifulSoup
from selenium import webdriver
import os

url = "https://www.bet365.com/#/AVR/B146/R^1/"
driver = webdriver.Chrome(executable_path=r"/home/Lucas/Documentos/chromedriver")

driver.get(url)

driver.maximize_window() #optional, if you want to maximize the browser
driver.implicitly_wait(60) ##Optional, Wait the loading if error

soup = BeautifulSoup(driver.page_source, 'html.parser') 

