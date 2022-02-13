# Import de bibliotecas necessárias para a geração da API
from flask import Flask
from flask import request
import pandas as pd
import os
import joblib
import json

# Importação do modelo por variável de ambiente
MODEL_PATH = os.environ['MODEL_PATH']
product_analyser = joblib.load(MODEL_PATH)

# Criação da API
api = Flask(__name__)

# Criação de uma rota chamando o método get para exibir informações ao usuário
@api.route("/info", methods=["GET"])
def info():
    return {"msg": "Registers categorization API, use /v1/categorize to classify your data"}

# Criação de uma rota chamando o método post para execução do modelo
@api.route("/v1/categorize", methods=["POST"])
def predict():
    # Definição de headers
    content_type = request.headers.get('Content-Type')
    # Verificação do tipo de conteúdo do arquivo enviado via post
    if (content_type == 'application/json'):
        # Leitura do json no elemento products com tratamento de erro
        try:
            json_file_list = request.json['products']
        except Exception as e:
            return {'api return': str(e)}, 400
        
        # Leitura dos elementos contidos no json e transformação em dicionário com tratamento de erro
        for dict_ in json_file_list:
            try:
                params = set(dict_.keys())
            except Exception as e:
                return {'Error:': str(e)}, 400
        # Verificação da falta de algum campo essencial ao modelo no arquivo passado, com tratamento de erro
        if not 'query' in params or not 'search_page' in params or not 'position' in params or not 'title' in params or not 'concatenated_tags' in params or not 'price' in params or not 'weight' in params or not 'express_delivery' in params:
            return {"Error": "File with missing fields"}, 400
        # Verificação da quantidade de campos recebidos e se ela casa com a quantidade esperada
        if len(params) != 14:
            return {"Error": "Categorization API waits for 14 fields but your json has " + str(len(params)) + " fields"}, 400
        # Transformação do dicionário em dataframe
        df = pd.DataFrame().from_dict(json_file_list)
        # Drop de colunas que devem ser desconsideradas pelo modelo
        df = df.drop(['product_id', 'seller_id', 'minimum_quantity', 'view_counts', 'order_counts', 'creation_date'], axis=1)
        # Retorno das variáveis preditas
        return {"categories": product_analyser.predict(df).tolist()}

# Criação de uma rota chamando o método post para salvar json de teste na variável TEST_PRODUCTS_PATH
@api.route("/save/json", methods=["POST"])
def save_json():
    # Definição de headers
    content_type = request.headers.get('Content-Type')
    # Verificação do tipo de conteúdo do arquivo enviado via post
    if (content_type == 'application/json'):
        # Leitura do json no elemento products com tratamento de erro
        try:
            json_file_list = request.json['products']
        except Exception as e:
            return {'api return': str(e)}, 400
        # Escrita de arquivo json para teste da API
        TEST_PRODUCTS_PATH = os.environ['TEST_PRODUCTS_PATH']
        with open(TEST_PRODUCTS_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_file_list, f,ensure_ascii=False)
        return json.dumps({'api return':'File saved with success'})
        
