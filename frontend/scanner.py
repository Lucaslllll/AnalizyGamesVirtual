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
        


