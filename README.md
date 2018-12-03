# SmartQueue
## SmartQueue Python Inteligencia Artificial
Quando for criar o projeto precisará criar o "modelo_finalizado", que é criado ao treinar e testar as bases de treino e teste.

### Comandos para executar localmente:
##### In Bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

FLASK_APP=application.py flask run

##### In PowerShell
py -3 -m venv env

env\scripts\activate

pip install -r requirements.txt

Set-Item Env:FLASK_APP ".\application.py"

flask run

### Comandos para publicar a aplicação no Azure
git commit -am "updated output"

git push azure master

### Create a Python web app in Azure App Service on Linux (Preview)
https://docs.microsoft.com/en-us/azure/app-service/containers/quickstart-python
