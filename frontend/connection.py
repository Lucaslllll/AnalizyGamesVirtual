import requests
import json




class Usuario(object):
    def do_login(self, email, password):
        valores = {"email": email, "password": password}
        requisicao = requests.post("http://localhost:8000/session/login", data=valores)
        
        if requisicao.status_code == 200:
            return True

        return False

    def buscar_dados(self):
        request = requests.get("http://localhost:8000/usuario")

        if request.status_code == 200:
            pass
        else:
            return request.status_code
        
        todos = json.loads(request.content)
        return todos
        #print(todos[0]['titulo'])


    def do_register(self, data, *args,**kwargs):
        #print(data)
        requisicao = requests.post("http://localhost:8000/usuario/", data=data)

        # codigo 201 é para create
        if requisicao.status_code == 201:
            return True

        print(requisicao.content)
        return False