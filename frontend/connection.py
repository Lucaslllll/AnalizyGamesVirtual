import requests
import json




class Usuario(object):
    def do_login(self, email, password):
        valores = {"email": email, "password": password}

        try:
            requisicao = requests.post("http://localhost:8000/accounts/session/login", data=valores)
        except:
            return None

        if requisicao.status_code == 200:
            return True

        return False
        

    def buscar_dados(self):

        try:
            request = requests.get("http://localhost:8000/accounts/usuario/")
        except:
            return None

        if request.status_code == 200:
            pass
        else:
            return request.status_code
        
        todos = json.loads(request.content)
        return todos
        

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