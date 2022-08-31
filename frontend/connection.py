import requests
import json


class Usuario(object):
    def buscar_dados(self):
        request = requests.get("http://localhost:8000/usuario")

        if request.status_code == 200:
            pass
        else:
            return request.status_code
        
        todos = json.loads(request.content)
        return todos
        #print(todos[0]['titulo'])

