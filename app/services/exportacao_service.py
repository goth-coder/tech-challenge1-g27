# Serviço para scraping e fallback de importação 
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import requests
from app.utils.exportacao_csv_utils import  load_exportacao_csv, save_exportacao_csv
from app.utils.config import EMBRAPA_BASE_URL
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

EXPORTACAO_SUBOPCOES = {
    'Vinhos de mesa': 'subopt_01',
    'Espumantes': 'subopt_02',
    'Uvas frescas': 'subopt_03',
    'Uvas passas': 'subopt_04',
    'Suco de uva': 'subopt_05',
}
# Obs. Os nomes das subopções acima podem ser diferentes. O site da EMBRAPA ta down, então n deu pra ver.


def fetch_exportacao_data_por_ano(ano):
    """
    Fetches product export data for all export sub-options for a given year.

    Args:
        ano (int): The year for which export data should be fetched.

    Returns:
        dict: A dictionary with the year as a string key and a nested dictionary containing
              product export data for all sub-option for a given year.
 
    Logging:
        Logs the start and successful completion of data fetching for each sub-option.
     
    """
    result = {}
    for tipo in EXPORTACAO_SUBOPCOES:
        logging.info(f"Buscando dados de exportação para o tipo '{tipo}' e ano {ano}")
        result[tipo] = fetch_exportacao_data(ano, tipo)
        logging.info("Dados de exportação obtidos com sucesso")
    return {str(ano): result}
 
 
def fetch_exportacao_data(ano, tipo):
    """
    Fetches product export data for a specific category and year from the Embrapa website.
    If the web request fails, falls back to loading data from a CSV file.
    
    Args:
        ano (int): The year for which to fetch export data.
        tipo (str): The export category (e.g., 'Vinhos de mesa', 'Espumantes').
    
    Returns:
        list of dict: Each dict contains keys such as 'ano', 'pais', 'quantidade', and 'valor'.
    ,tipo
    Logging:
        Logs the initiation of the web request.
        Logs errors encountered during the request or parsing.
        Logs when falling back to loading data from a CSV file.
    """ 
    subopcao = EXPORTACAO_SUBOPCOES.get(tipo)  
    url = f"{EMBRAPA_BASE_URL}{ano}&opcao=opt_06&subopcao={subopcao}"
    try:
        logging.info(f"Iniciando requisição para URL: {url}")

        response = requests.get(url, timeout=14)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        time.sleep(1) 
        return parse_exportacao_data(soup, ano,tipo)
        
    except Exception as e:
        logging.error(
            f"❌ [fetch_exportacao_data] Falha ao processar dados: "
            f"tipo='{tipo}', ano={ano}, url='{url}'. Erro: {e}\n"
        )
        logging.info(f"Fallback para CSV: tipo='{tipo}', ano={ano}")
    
        return load_exportacao_csv(ano, tipo)
  

def parse_exportacao_data(soup, ano,tipo):
    """
    Parses product export data from an HTML table and returns a list of dictionaries with country, quantity, and value.
    Args:
        soup (bs4.BeautifulSoup): Parsed HTML content containing the export data table.
        ano (int or str): Year associated with the export data.
        
    Returns:
        list of dict: A list where each dict contains:
            'ano' (int): The year of the export data.
            'pais' (str): The country name.
            'quantidade' (float): The quantity exported.
            'valor' (float): The value of the export.

    Notes: 
        If the table is not found, returns an empty list.
        Non-numeric values in 'quantidade' and 'valor' are replaced with 0.
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
    save_exportacao_csv(data, tipo)  # Salva os dados no CSV
    return data


if __name__ == "__main__":
    "For debugging"
    result = fetch_exportacao_data('2023', 'Vinhos de mesa')
    result2 = fetch_exportacao_data_por_ano('2023')
    print(result)
    print(result2)