# Serviço para scraping e fallback de processamento
import requests
from app.utils.config import EMBRAPA_BASE_URL
from app.utils.config import PROCESS_CSV_MAP as CSV_MAP
from app.utils.csv_utils import load_generic_csv
from app.utils.parse_utils import parse_int
from bs4 import BeautifulSoup
import requests
import os

PROCESSAMENTO_SUBOPCOES = {
    'viniferas': 'subopt_01',
    'americanas': 'subopt_02',
    'mesa': 'subopt_03',
    'semclass': 'subopt_04',
}

def fetch_processamento_data_por_ano(ano):
    """
    Busca dados de todas as subopções de processamento para o ano informado.
    """
    result = {}
    fonte_final = "Dados internos - Embrapa .csv"  # Assume CSV por padrão
    
    for tipo, subopcao in PROCESSAMENTO_SUBOPCOES.items():
        data_with_source = fetch_processamento_data(ano, tipo)
        result[tipo] = data_with_source["dados"]
        # Se algum dos dados vier do site, define fonte como site
        if data_with_source["fonte"] == "Embrapa - Sistema de dados vitivinícolas":
            fonte_final = "Embrapa - Sistema de dados vitivinícolas"
    
    return {
        str(ano): result,
        "fonte": fonte_final
    }

def fetch_processamento_data(ano, tipo):
    """
    Busca dados de uma subopção específica (viniferas, americanas, mesa, semclass) para o ano informado.
    """
    subopcao = PROCESSAMENTO_SUBOPCOES.get(tipo)
    url = f"{EMBRAPA_BASE_URL}{ano}&opcao=opt_03&subopcao={subopcao}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        data = parse_processamento_html(soup)
        return {
            "dados": data,
            "fonte": "Embrapa - Sistema de dados vitivinícolas"
        }
    except Exception:
        csv_data = load_generic_csv(
                tipo=tipo,
                ano=ano,
                csv_map=CSV_MAP,
                id_col_name='cultivar',
                value_col_name=None,
                output_keys={'id': 'produto', 'qtd': 'quantidade'}
            )
        return {
            "dados": csv_data,
            "fonte": "Dados internos - Embrapa .csv"
        }

def parse_processamento_html(soup):
    """
    Faz o parsing do HTML de processamento (tabela principal).
    Retorna lista de dicts: [{cultivar, quantidade}]
    """
    table = soup.find('table', {'class': 'tb_base tb_dados'})
    if not table:
        return []
    rows = table.find('tbody').find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue
        cultivar = cols[0].get_text(strip=True)
        quantidade = parse_int(cols[1].get_text())
        if cultivar:
            data.append({'cultivar': cultivar, 'quantidade': quantidade})
    return data
