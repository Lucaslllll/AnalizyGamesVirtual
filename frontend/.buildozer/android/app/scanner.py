## primeira forma

from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, build_opener, Request, ProxyHandler, HTTPSHandler
import ssl
# import pandas de alguma forma o android não tem alguma lib c++ 
# necessária para a utilização do pandas


class JogosStats(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.times = 0
        self.find_two_times_var = False
        self.times_cabecalho = 0
        self.cabecalho_pass_var = False
        self.final_text = []


    def get(self):
        context = ssl._create_unverified_context()
        url = "https://www.placardefutebol.com.br/brasileirao-serie-a"
        # r = urllib.request.urlopen('https://google.com', context=context)
        
        try:
            html = urlopen(url, context=context).read()
        except:
            return {}
            
        soup = BeautifulSoup(html, 'html.parser')


        tabela_classificacao = soup.find_all("table", {"class": "table standing-table"})
        tabela_classificacao_str = str(tabela_classificacao)

        for tags in soup(["script", "style"]):
            tags.extract()

        text = soup.get_text()

        # print("text cru pelo get_text = "+text)

        new_text = text.rsplit("\n")

        # print("lista crua = "+str(new_text))

        for i in range(0, len(new_text)):
            if i > len(new_text)-1:
                continue
            if new_text[i] == '':
                continue


            self.cabecalho_pass(new_text[i])
            if self.cabecalho_pass_var == False:
                continue 

            self.find_two_times(new_text[i])
            if self.find_two_times_var == False:
                self.final_text.append(new_text[i])
            else:
                continue

        
        self.final_text.pop(0)
        self.final_text.insert(0, "pos")

        # print("final = "+str(self.final_text))

        col = 0
        dic = {}
        row = len(self.final_text)/8
        
        contador = 0
        lista = []
        for e in self.final_text:
            

            if contador < 8:
                dic[e] = []
                lista.append(e)
            elif col < 8:
                dic[lista[col]].append(e)
            elif col >= 8:
                col = 0
                dic[lista[col]].append(e)
                
            contador += 1 
            col += 1


        # print("passou pelo for = "+str(dic))
        # print("============================")
        # print(dic)

        return dic



    def cabecalho_pass(self, text):
        if text == "Classificação - Campeonato Brasileiro":
            self.times_cabecalho += 4

        if self.times_cabecalho >= 4:
            self.cabecalho_pass_var = True


    def find_two_times(self, text):


        if text == "Artilheiros - Campeonato Brasileiro":
            self.times = 2

        if self.times >= 2:
            self.find_two_times_var = True
        

# stats = JogosStats()
# print(stats.get())
# stats.get()
# print("tamanho"+str(len(stats.get())))


# df = pandas.read_html(tabela_classificacao_str)[0]
# dic = pandas.DataFrame.to_dict(df)



        # return dic

# with open("site.txt", "w") as data:
#     # data.write(soup.prettify())
#     data.write(str(dic))



## segunda forma

# from soccerapi.api import Api888Sport
# from soccerapi.api import ApiUnibet
# from soccerapi.api import ApiBet365

# class JogosStats(object):
#     def get(self):
#         api = Api888Sport()
#         url = "https://www.888sport.com/#/filter/football/brazil/serie_a"
#         # url = 'https://www.888sport.com/football/brazil/brazil-serie-a-t-330348/'
#         odds = api.odds(url)

#         return odds


## outra forma


# from bs4 import BeautifulSoup
# from selenium import webdriver
# import os

# url = "https://www.bet365.com/#/AVR/B146/R^1/"
# driver = webdriver.Chrome(executable_path=r"/home/Lucas/Documentos/chromedriver")

# driver.get(url)

# driver.maximize_window() #optional, if you want to maximize the browser
# driver.implicitly_wait(60) ##Optional, Wait the loading if error

# soup = BeautifulSoup(driver.page_source, 'html.parser') 



## quarta forma, mas precisa pagar



# import requests

# url = "https://betsapi2.p.rapidapi.com/v1/bet365/result"

# querystring = {"event_id":"<REQUIRED>"}

# headers = {
# 	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
# 	"X-RapidAPI-Host": "betsapi2.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)


## quinta forma


# from bs4 import BeautifulSoup
# import requests

# url = 'https://www.bet365.com/#'
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.0 Safari/537.36","Referer":"https://www.bet365.com/","X-Net-Sync-Term":"AiMAAwAyAAFPkK81/1zvXq0NpdL4a5LQj/vUOYL4QI325x9STGdew2hmDR+Ak+k5cpjrZrUnXAglzmiNX50KuCVBWNVAb+7CwI/Ps8pt9jSaFUN/qlWAorANEjJlzXJyAgaUz5gbs15aY5nvIrRmuD81D8XrTVE65e8g2gruSYnwD8nLJ0nR1Z4VeXsVyj+2aWNJ6EDUbka0Z4m52EqgHg3cgIfYhpcVZMa3sJK5pMoss8Zdbnhrt1sydmzQg8+oFSRLkzGEQQUBOBdZQ7BlPhOKSmBD5+SdIZ67eYmGLhYxkl/4ZEzvMBlOkcqNAFLaCve8RQcMST4bdbKUte7G3dMcso6pIXcWcAigk6LdYV6WD7dYnVAwNfrmqRSqm8ykkSNQHCai8gFNwpfsmNKndJ/4hIrOaGOshFk8PYfZzC1NACovarqn6RY1GOv3xnCkvnu+CXxJoLB8HlCJ0+dantOFuZTzExizJrfhAm9hVnTy1Uw6Io2IZMddApqN5/kAo8JUXQEh7134riPEF5bvQv+fk3VFO7O2hvYknAy2w8s+pd2dDdSW7AJmHq5Y6aTVU3KVqu/58nRQfjMS5e2IuZe9//A="}
# payload = {'action':'info',
#                'action':'info',
#                'api_key':'something'
#                }


# soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')


# print(soup.prettify())

# while True:
#     for a in soup.select('.result__a'):
#         yield a['href'

#     f = soup.select_one('input[value="Next"]')
#     if not f:
#         break

#     params = {i['name']: i.get('value', '') for i in f.find_parent('form').select('input[name]')}
#     soup = BeautifulSoup(requests.post(url, params=params, headers=headers).content, 'html.parser')






# from selenium import webdriver  
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options

# CHROME_PATH = '/usr/bin/firefox'
# WINDOW_SIZE = "1920,1080"

# firefox_options = Options()
# firefox_options.add_argument("--headless")
# firefox_options.add_argument("--window-size=%s" % WINDOW_SIZE)
# # firefox_options.binary_location = "/home/Lucas/Documentos/geckodriver"

# browser = webdriver.Firefox(executable_path=r"/home/Lucas/Documentos/geckodriver",  options=firefox_options)  
# browser.get('https://www.bet365.com/#/AVR/B146/R^1/')  
# # input =  browser.find_element_by_css_selector('input[type="text"]')
# # input.send_keys('koaning.com')

# # WebDriverWait(browser, 5).until(EC.presence_of_element_located((inputElement.send_keys(Keys.ENTER))))

# browser.quit()





# from urllib.request import urlopen
# from bs4 import BeautifulSoup

# url = "https://www.placardefutebol.com.br/brasileirao-serie-a"
# html = urlopen(url).read()
# soup = BeautifulSoup(html, features="html.parser")

# # kill all script and style elements
# for script in soup(["script", "style"]):
#     script.extract()    # rip it out

# # get text
# text = soup.get_text()

# # break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# # break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# # drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)

# print(text)
