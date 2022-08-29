import requests
import json

def buscar_dados():
    request = requests.get("http://localhost:8000/api/todo")
    todos = json.loads(request.content)
    print(todos)
    print(todos[0]['titulo'])

