from flask import Flask, jsonify
import requests
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SWAGGER'] = {
    'title': 'API de Produção de Vinho',
    'uiversion': 3
}

swagger = Swagger(app)


## observe os dados do json retornado das rotas sao os mesmo do .csv
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    else:
        return None
	

@app.route('/hello', methods=['GET'])
@auth.login_required
def hello():
    """Rota de exemplo para verificar autenticação"""
    return jsonify({"message": f"Hello, {auth.current_user()}!"})


def fetch_data(year):
    """Faz a requisição para a página e retorna os dados estruturados"""
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02"
    html_content = requests.get(url)
    
    if html_content.status_code != 200:
        return None
    
    soup = BeautifulSoup(html_content.text, "html.parser")
    
    # Extrair dados da tabela
    table = soup.find('table', {'class': 'tb_dados'})
    if not table:
        return None
    
    rows = table.find('tbody').find_all('tr')
    
    # Estrutura para armazenar os dados
    wine_data = {
        "vinho_de_mesa": {
            "total": 0,
            "detalhes": {
                "tinto": 0,
                "branco": 0,
                "rosado": 0
            }
        },
        "vinho_fino_de_mesa": {
            "total": 0,
            "detalhes": {
                "tinto": 0,
                "branco": 0,
                "rosado": 0
            }
        },
        "suco": {
            "total": 0,
            "detalhes": {
                "suco_de_uva_integral": 0,
                "suco_de_uva_concentrado": 0,
                "suco_de_uva_adoçado": 0
            }
        }
    }
    
    current_category = None
    
    for row in rows:
        cols = row.find_all('td')
        item_name = cols[0].text.strip()
        quantity_text = cols[1].text.strip()
        
        # Verificar se o valor é um traço ou está vazio
        if quantity_text == '-' or not quantity_text:
            quantity = 0
        else:
            # Remover pontos e converter para inteiro
            quantity = int(re.sub(r'\.', '', quantity_text))
        
        # Identificar a categoria principal ou subcategoria
        if 'VINHO DE MESA' == item_name:
            current_category = 'vinho_de_mesa'
            wine_data[current_category]['total'] = quantity
        elif 'VINHO FINO DE MESA' in item_name:
            current_category = 'vinho_fino_de_mesa'
            wine_data[current_category]['total'] = quantity
        elif 'SUCO' == item_name:
            current_category = 'suco'
            wine_data[current_category]['total'] = quantity
        # Subcategorias
        elif current_category:
            item_name_lower = item_name.lower()
            if current_category in ['vinho_de_mesa', 'vinho_fino_de_mesa']:
                if 'tinto' in item_name_lower:
                    wine_data[current_category]['detalhes']['tinto'] = quantity
                elif 'branco' in item_name_lower:
                    wine_data[current_category]['detalhes']['branco'] = quantity
                elif 'rosado' in item_name_lower:
                    wine_data[current_category]['detalhes']['rosado'] = quantity
            elif current_category == 'suco':
                if 'integral' in item_name_lower:
                    wine_data[current_category]['detalhes']['suco_de_uva_integral'] = quantity
                elif 'concentrado' in item_name_lower:
                    wine_data[current_category]['detalhes']['suco_de_uva_concentrado'] = quantity
                elif 'adoçado' in item_name_lower:
                    wine_data[current_category]['detalhes']['suco_de_uva_adoçado'] = quantity
    
    return wine_data

@app.route('/production', methods=['GET'])
@auth.login_required
def get_production():
    """
    Retorna os dados de produção de todos os anos (2010-2023)
    ---
    security:
      - basicAuth: []
    responses:
      200:
        description: Dados de produção de vinho
        schema:
          type: object
          properties:
            ano:
              type: object
              properties:
                '2010':
                  type: object
                  properties:
                    vinho_de_mesa:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            tinto:
                              type: integer
                            branco:
                              type: integer
                            rosado:
                              type: integer
                    vinho_fino_de_mesa:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            tinto:
                              type: integer
                            branco:
                              type: integer
                            rosado:
                              type: integer
                    suco:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            suco_de_uva_integral:
                              type: integer
                            suco_de_uva_concentrado:
                              type: integer
                            suco_de_uva_adoçado:
                              type: integer
    """
    result = {"ano": {}}
    
    for year in range(2010, 2024):
        year_data = fetch_data(year)
        if year_data:
            result["ano"][str(year)] = year_data
    
    return jsonify(result)

@app.route('/production/<int:year>', methods=['GET'])
def get_production_by_year(year):
    """Retorna os dados de produção de um ano específico
    ---
    security:
      - basicAuth: []
    responses:
      200:
        description: Dados de produção de vinho
        schema:
          type: object
          properties:
            ano:
              type: object
              properties:
                '2010':
                  type: object
                  properties:
                    vinho_de_mesa:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            tinto:
                              type: integer
                            branco:
                              type: integer
                            rosado:
                              type: integer
                    vinho_fino_de_mesa:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            tinto:
                              type: integer
                            branco:
                              type: integer
                            rosado:
                              type: integer
                    suco:
                      type: object
                      properties:
                        total:
                          type: integer
                        detalhes:
                          type: object
                          properties:
                            suco_de_uva_integral:
                              type: integer
                            suco_de_uva_concentrado:
                              type: integer
                            suco_de_uva_adoçado:
                              type: integer
    """
    if year < 2010 or year > 2023:
        return jsonify({"error": "Ano deve ser entre 2010 e 2023"}), 400
    
    year_data = fetch_data(year)
    if not year_data:
        return jsonify({"error": f"Dados para o ano {year} não encontrados"}), 404
    
    result = {"ano": {str(year): year_data}}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)