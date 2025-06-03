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
    for tipo, subopcao in PROCESSAMENTO_SUBOPCOES.items():
        result[tipo] = fetch_processamento_data(ano, tipo)
    return {str(ano): result}

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
        return parse_processamento_html(soup)
    except Exception:
        return load_generic_csv(
                tipo=tipo,
                ano=ano,
                csv_map=CSV_MAP,
                id_col_name='cultivar',
                value_col_name=None,
                output_keys={'id': 'produto', 'qtd': 'quantidade'}
            )

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
