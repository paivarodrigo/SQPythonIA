import requests
import numpy as np
import pickle
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/train', methods=['GET'])
def train():
    response = requests.get('http://smartqueueapi.azurewebsites.net/api/estudos/buscardadostreinoia')
    response_json = response.json()
    columns = ['horaSolicitacao', 'horaCheckin', 'qtdPessoas', 'qtdEnt', 'qtdPrincipal', 'qtdBebidas', 'qtdSobremesas', 'fds', 'noite', 'minutosUtilizados']    
    df = pd.DataFrame(response_json, columns = columns)
    df_ordenada = df.sort_values(by='horaCheckin', ascending=False)
    maior_valor = df_ordenada.values[0,1] #será utilizado para mostrar o valor da saida
    df_tratada = df.div(maior_valor)
    df_x = df_tratada.iloc[:,:-1]
    df_y = df_tratada.iloc[:,9]
    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.1, random_state=4)
    model = MLPRegressor(activation='tanh', alpha=1e-05, batch_size='auto', beta_1=0.9,
                         beta_2=0.999, early_stopping=True, epsilon=1e-09,
                         hidden_layer_sizes=(90, 40), learning_rate='constant',
                         learning_rate_init=0.001, max_iter=200, momentum=0.9,
                         nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
                         solver='adam', tol=0.0001, validation_fraction=0.1, verbose=False,
                         warm_start=False)
    model.fit(x_train, y_train)
    filename = 'modelo_finalizado.sav'
    pickle.dump(model, open(filename, 'wb'))
    accuracy = model.score(df_x, df_y)
    return 'Acurácia: ' + str(accuracy)

@app.route('/test', methods=['GET'])
def test():
    response = requests.get('http://smartqueueapi.azurewebsites.net/api/estudos/buscardadostesteia')
    response_json = response.json()
    columns = ['horaSolicitacao', 'horaCheckin', 'qtdPessoas', 'qtdEnt', 'qtdPrincipal', 'qtdBebidas', 'qtdSobremesas', 'fds', 'noite', 'minutosUtilizados']    
    df = pd.DataFrame(response_json, columns = columns)
    df_ordenada = df.sort_values(by='horaCheckin', ascending=False)
    maior_valor = df_ordenada.values[0,1] #será utilizado para mostrar o valor da saida
    df_tratada = df.div(maior_valor)
    df_x = df_tratada.iloc[:,:-1]
    df_y = df_tratada.iloc[:,9]
    filename  ='modelo_finalizado.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    prediction = loaded_model.predict(df_x)
    prediction = np.multiply(prediction, maior_valor)
    prediction.sort()
    final_result = np.average(prediction[:5])
    accuracy = loaded_model.score(df_x, df_y)    
    return 'Resultado Final: ' + str(final_result) + ' Acurácia: ' + str(accuracy)

@app.route('/run/<int:quantity>')
def run(quantity):
    response = requests.get('http://smartqueueapi.azurewebsites.net/api/estudos/buscardadosexecucao')
    response_json = response.json()
    columns = ['horaSolicitacao', 'horaCheckin', 'qtdPessoas', 'qtdEnt', 'qtdPrincipal', 'qtdBebidas', 'qtdSobremesas', 'fds', 'noite']    
    df = pd.DataFrame(response_json, columns = columns)
    df_ordenada = df.sort_values(by='horaCheckin', ascending=False)
    maior_valor = df_ordenada.values[0,1] #será utilizado para mostrar o valor da saida
    df_tratada = df.div(maior_valor)
    filename  ='modelo_finalizado.sav'
    loaded_model = pickle.load(open(filename, 'rb'))    
    prediction = loaded_model.predict(df_tratada)
    prediction = np.multiply(prediction, maior_valor)
    prediction = np.ceil(prediction)
    prediction.sort()
    responsePred = []
    for i in range(quantity):
        if i < len(prediction):
            responsePred.append(prediction[i])
        else:
            responsePred.append(np.ceil((responsePred[0] / 5) + responsePred[-1]))
    return jsonify({'tempos': responsePred})