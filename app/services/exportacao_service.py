# Serviço para scraping e fallback de exportação
import requests
from app.utils.config import EMBRAPA_BASE_URL
from app.utils.config import EXPORT_CSV_MAP as CSV_MAP
from app.utils.csv_utils import load_generic_csv
from app.utils.parse_utils import parse_int
from bs4 import BeautifulSoup

EXPORTACAO_SUBOPCOES = {
    'vinhos': 'subopt_01',      # VINHO DE MESA
    'espumantes': 'subopt_02',  # ESPUMANTES
    'frescas': 'subopt_03',     # UVAS FRESCAS
    'suco': 'subopt_04',        # SUCO DE UVA
}

def fetch_exportacao_data_por_ano(ano):
    """
    Busca dados de todas as subopções de exportação para o ano informado.
    """
    result = {}
    for tipo, subopcao in EXPORTACAO_SUBOPCOES.items():
        result[tipo] = fetch_exportacao_data(ano, tipo)
    return {str(ano): result}

def fetch_exportacao_data(ano, tipo):
    """
    Busca dados de uma subopção específica (vinhos, espumantes, frescas, suco) para o ano informado.
    """
    subopcao = EXPORTACAO_SUBOPCOES.get(tipo)
    if not subopcao:
        return []
    
    url = f"{EMBRAPA_BASE_URL}{ano}&opcao=opt_06&subopcao={subopcao}"
    try:
        resp = requests.get(url, timeout=10) 
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        return parse_exportacao_html(soup)
    except Exception:
        return load_generic_csv(
                tipo=tipo,
                ano=ano,
                csv_map=CSV_MAP,
                id_col_name='pais',
                value_col_name='valor',
                output_keys={'id': 'pais', 'qtd': 'quantidade', 'val': 'valor'}
            )

def parse_exportacao_html(soup):
    """
    Faz o parsing do HTML de exportação (tabela principal).
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
