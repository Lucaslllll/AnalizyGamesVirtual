import requests
import json


class Authenticat(object):
    def __init__(self):
        self.token_access = None
        self.token_refresh = None

    def do_auth(self):
        valores = {
            "username":"admin",
            "password":"root1234"
        }

        try:
            requisicao = requests.post("http://localhost:8000/token", data=valores)
        except:
            return None

        dic_content = requisicao.json()
        if requisicao.status_code == 200:
            self.token_access = dic_content["access"]
            self.token_refresh = dic_content["refresh"]
        elif requisicao.status_code == 401:
            return False

        return True


        # return token acess if auth is true

    def do_refresh(self, refresh):
        valores = {
            "refresh":self.token_refresh,
        }
        

        try:
            requisicao = requests.post("http://localhost:8000/token/refresh", data=valores)
        except:
            return None

        dic_content = requisicao.json()
        self.token_access = dic_content["access"]

        return self.token_access
        # return token if send refresh token


    def get_token(self):
        return self.token_access


    def get_token_refresh(self):
        return self.token_refresh


class Usuario(object):
    token_access = None
    token_refresh = None

    def do_login(self, email, password):
        valores = {"email": email, "password": password}

        auth = Authenticat()
        resposta = auth.do_auth()
        
        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            # print(self.token_access)
            
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            try:
                requisicao = requests.post("http://localhost:8000/accounts/session/login", 
                                            data=valores, headers=head)
            except:
                return "Error ao Fazer o Login"
        
            if requisicao.status_code == 200:
                return {
                            "token_access":self.token_access, 
                            "token_refresh":self.token_refresh,
                            "dados": requisicao.json()
                        }
            elif requisicao.status_code == 400:
                return "Dados incorretos"

            return "Error Inesperado"
           
        elif resposta == False:
            return "Credencias Inválidas"
            
        elif resposta == None:
            return "Problemas em contatar o servidor!"





    def buscar_dados(self, pk):
        auth = Authenticat()
        resposta = auth.do_auth()


        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            try:
                request = requests.get("http://localhost:8000/accounts/usuario/{}".format(pk), headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"

            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"
        

    def do_register(self, data, *args,**kwargs):
        #print(data)
        
        try:
            requisicao = requests.post("http://localhost:8000/accounts/usuario/", data=data)
        except:
            return None

        # codigo 201 é para create
        if requisicao.status_code == 201:
            return True

        # print(requisicao.content)
        return False


class Noticias(object):
    token_access = None
    token_refresh = None

    def get(self):
        auth = Authenticat()
        resposta = auth.do_auth()


        if resposta == True:
            self.token_access = auth.get_token()
            self.token_refresh = auth.get_token_refresh()
            head = {'Authorization': 'Bearer {}'.format(self.token_access)}

            try:
                request = requests.get("http://localhost:8000/noticias", headers=head)
            except:
                return "Error ao Fazer Requisição ao Servidor"

            if request.status_code == 200:
                return request.json()
            elif request.status_code == 401:
                return "Sem Autorização"
            else:
                return "Erro Inesperado"
        elif resposta == False:
            return "Credencias Inválidas"
        else:
            return "Problemas em contatar o servidor!"

# news = Noticias()

# print(news.get())
# print(news.token_access)
