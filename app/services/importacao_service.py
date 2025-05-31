# Serviço para scraping e fallback de importação
import requests
from app.utils.config import EMBRAPA_BASE_URL
from app.utils.importacao_csv_utils import load_importacao_csv
from app.utils.parse_utils import parse_int
from bs4 import BeautifulSoup

IMPORTACAO_SUBOPCOES = {
    'vinhos': 'subopt_01',      # VINHO DE MESA
    'espumantes': 'subopt_02',  # ESPUMANTES
    'frescas': 'subopt_03',     # UVAS FRESCAS
    'passas': 'subopt_04',      # UVAS PASSADAS
    'suco': 'subopt_05',        # SUCO DE UVA
}

def fetch_importacao_data_por_ano(ano):
    """
    Busca dados de todas as subopções de importação para o ano informado.
    """
    result = {}
    for tipo, subopcao in IMPORTACAO_SUBOPCOES.items():
        result[tipo] = fetch_importacao_data(ano, tipo)
    return {str(ano): result}

def fetch_importacao_data(ano, tipo):
    """
    Busca dados de uma subopção específica (vinhos, espumantes, frescas, passas, suco) para o ano informado.
    """
    subopcao = IMPORTACAO_SUBOPCOES.get(tipo)
    if not subopcao:
        return []
    
    url = f"{EMBRAPA_BASE_URL}{ano}&opcao=opt_05&subopcao={subopcao}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        return parse_importacao_html(soup)
    except Exception:
        return load_importacao_csv(tipo, ano)

def parse_importacao_html(soup):
    """
    Faz o parsing do HTML de importação (tabela principal).
    Retorna lista de dicts: [{'pais': ..., 'quantidade': ..., 'valor': ...}]
    """
    table = soup.find('table', {'class': 'tb_base tb_dados'})
    if not table:
        return []
    
    tbody = table.find('tbody')
    if not tbody:
        return []
    
    rows = tbody.find_all('tr')
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 3:
            continue
        
        pais = cols[0].get_text(strip=True)
        quantidade_text = cols[1].get_text(strip=True)
        valor_text = cols[2].get_text(strip=True)
        
        # Parse quantidade
        if quantidade_text == '-' or quantidade_text == '':
            quantidade = 0
        else:
            quantidade = parse_int(quantidade_text)
        
        # Parse valor
        if valor_text == '-' or valor_text == '':
            valor = 0
        else:
            valor = parse_int(valor_text)
        
        if pais:
            data.append({
                'pais': pais,
                'quantidade': quantidade,
                'valor': valor
            })
    
    return data
