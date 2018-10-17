import json, requests
import urllib3
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
#    response = requests.get("http://smartqueueapi.azurewebsites.net/api/produtos/listarprodutos")
    
    data = {"Email":"jefferson.teste@gmail.com", "Senha":"123456"}
#    response = requests.post('http://smartqueueapi.azurewebsites.net/api/usuarios/logar', data = data)
# =============================================================================
#     req = u.Request('http://smartqueueapi.azurewebsites.net/api/usuarios/logar')
#     req.add_header('Content-Type','application/json')
#     response = u.urlopen(req, data)
#     
# =============================================================================
    
    encoded_body = json.dumps({ "Email": "jefferson.teste@gmail.com", "Senha": "123456" })
    http = urllib3.PoolManager()

    response = http.request('POST', 'http://smartqueueapi.azurewebsites.net/api/usuarios/logar',
                 headers={'Content-Type': 'application/json'},
                 body=encoded_body)
    return str(json.loads(response.data.decode('utf-8')))

@app.route("/get")
def gette():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://smartqueueapi.azurewebsites.net/api/estudos/buscardadosexecucao')
    return str(json.loads(r.data.decode('utf-8')))
@app.route("/geti")
def getti():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://smartqueueapi.azurewebsites.net/api/estudos/buscardadostreinoia')
    return str(json.loads(r.data.decode('utf-8')))
@app.route("/geto")
def getto():
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://smartqueueapi.azurewebsites.net/api/estudos/buscardadostesteia')
    return str(json.loads(r.data.decode('utf-8')))