# Importação de bibliotecas usadas para teste
from os.path import dirname, realpath
from flask import json
import os
import json
import pandas as pd
import requests

# Captura do diretório com arquivos
basedir = os.path.abspath(os.path.dirname(__file__))

#######################################################################################################
# Cenário 1: teste da API em ambiente perfeito (Sucesso)
# Leitura do csv com os dados de teste removendo a coluna a ser predita
df = pd.read_csv(basedir + '/../data/test_products.csv')
df = df.drop(['category'], axis=1)

# Conversão do dataframe em json
df_json = df.to_json(orient='records', force_ascii=False)
product_list_json = json.loads(df_json)

# Requisição na API com o json já formado e print de resultados
newHeaders = {'Content-type': 'application/json'}
r = requests.post('http://localhost:5000/v1/categorize', json={'products': product_list_json}, headers=newHeaders)
print('Cenário 1 retorno: ' + str(r))
print(json.loads(r.content))

#######################################################################################################
# Cenário 2: teste da API com json com atributo faltante (Falha)
# Cria cópia do df para novo teste
df2 = df.copy()
df2 = df2.drop(['query'], axis=1)

# Conversão do dataframe em json para teste no cenário 2
df_json2 = df2.to_json(orient='records', force_ascii=False)
product_list_json2 = json.loads(df_json2)

# Requisição na API com o json já formado e print de resultados
newHeaders = {'Content-type': 'application/json'}
r = requests.post('http://localhost:5000/v1/categorize', json={'products': product_list_json2}, headers=newHeaders)
print('Cenário 2 retorno: ' + str(r))
print(json.loads(r.content))

#######################################################################################################
# Cenário 3: teste da API com json vazio (Falha)
# Requisição na API com o json vazio e print de resultados
newHeaders = {'Content-type': 'application/json'}
r = requests.post('http://localhost:5000/v1/categorize', json={}, headers=newHeaders)
print('Cenário 3 retorno: ' + str(r))
print(json.loads(r.content))

#######################################################################################################
# Cenário 4: teste da API com json com campos extras  (Falha)
# Cria cópia do df para novo teste
df3 = df.copy() 
# Criação de nova coluna para teste
new = []
for i in range(0, len(df3)):
    new.append(i)
df3['New'] = new

df_json3 = df3.to_json(orient='records', force_ascii=False)
product_list_json3 = json.loads(df_json3)

# Requisição na API com o json já formado e print de resultados
newHeaders = {'Content-type': 'application/json'}
r = requests.post('http://localhost:5000/v1/categorize', json={'products': product_list_json3}, headers=newHeaders)
print('Cenário 4 retorno: ' + str(r))
print(json.loads(r.content))

#######################################################################################################
# Escrita de arquivo json para teste da API (foi salvo tanto localmente quanto na variável do servidor via API)
with open(basedir + '/test_products_path.json', 'w', encoding='utf-8') as f:
    json.dump({'products': product_list_json}, f, ensure_ascii=False)

# Requisição na API com o json formado para escrita do arquivo no servidor
newHeaders = {'Content-type': 'application/json'}
r = requests.post('http://localhost:5000/save/json', json={'products': product_list_json}, headers=newHeaders)
print(r)
print(json.loads(r.content))





