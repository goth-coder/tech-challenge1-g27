# Serviço para scraping e fallback de importação 
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import requests
from app.utils.csv_utils import load_csv_fallback
from app.utils.importacao_csv_utils import CSV_MAP, load_importacao_csv, save_importacao_csv
import warnings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IMPORTACAO_SUBOPCOES = {
    'Vinhos de mesa': 'subopt_01',
    'Espumantes': 'subopt_02',
    'Uvas frescas': 'subopt_03',
    'Uvas passas': 'subopt_04',
    'Suco de uva': 'subopt_05',
}

   
def fetch_all():
    """
    Busca dados de todas as subopções de importação para os anos informados e cria um arquivo para cada subopção contendo todos os anos.
    """
    
    for tipo, subopcao in IMPORTACAO_SUBOPCOES.items(): 
        result = []
        for ano in range(1970, 2025): 
            print('ANO', ano)
            try: 
                data = fetch_importacao_data(ano, tipo) 
                if not data:
                    logging.warning(f"Dados não encontrados para o ano {ano}.")
                    continue
                result.extend(data)
                logging.info(f"Dados coletados com sucesso para o ano {ano}, tipo {tipo}")
                 
            except Exception as e:
                logging.error(f"Erro ao buscar dados para o ano {ano} tipo {tipo}: {e}")
 
        save_importacao_csv(result,tipo)


def fetch_importacao_data(ano, tipo):
    """
    Scrape todos os blocos de importação do site da Embrapa para o ano informado.
    Se falhar, faz fallback para o CSV, retornando todos os dados (se ano=None) ou apenas do ano (se ano informado).
    Retorna uma lista de dicts: [{categoria, produto, ano, valor}]
    """
    subopcao = IMPORTACAO_SUBOPCOES.get(tipo) if tipo else 'Vinhos de mesa'
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_05&subopcao={subopcao}"
    try:
        logging.info(f"Iniciando requisição para URL: {url}")

        response = requests.get(url, timeout=14)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return parse_importacao_data(soup, ano,tipo)
        
    except Exception as e:
        logging.error(f"Erro ao processar dados de {tipo} para o ano {ano}: {e}")
        logging.info(f"Realizando fallback para CSV de {tipo}, ano {ano}")        
        return load_importacao_csv(ano, tipo)
  

def parse_importacao_data(soup, ano,tipo):
    """
    Parses import data from an HTML table and returns a list of dictionaries with country, quantity, and value.
    Args:
        soup (bs4.BeautifulSoup): Parsed HTML content containing the import data table.
        ano (int or str): Year associated with the import data.
    Returns:
        list of dict: A list where each dict contains:
            - 'ano' (int): The year of the import data.
            - 'pais' (str): The country name.
            - 'quantidade' (float): The quantity imported.
            - 'valor' (float): The value of the import.
    Notes:
        - Expects the table to have the class 'tb_dados'.
        - If the table is not found, returns an empty list.
        - Non-numeric values in 'quantidade' and 'valor' are replaced with 0.
    """ 
    table = soup.find('table', {'class': 'tb_dados'})
    if not table:
        return []
    
    rows = table.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td') 
        row_list = [col.get_text(strip=True).replace('.', '').replace('-', '0') for col in cols]            
        if row_list != []: 
            try:
                pais, quantidade, valor = row_list[:3]                
            except Exception as e:
                logging.error(f"Erro ao processar linha: {row_list}, erro: {e}")
                break
            data.append({
                'ano':int(ano),      
                'pais': pais,
                'quantidade': float(quantidade),                    
                'valor': float(valor)
            }) 

    return data




if __name__ == "__main__":
    fetch_all()