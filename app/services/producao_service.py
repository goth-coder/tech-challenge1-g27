# Serviço para scraping e fallback de produção
from app.utils.config import EMBRAPA_BASE_URL, CSV_PATH_PRODUCAO
from app.utils.csv_utils import load_csv_fallback
from bs4 import BeautifulSoup
import re
import requests


def fetch_producao_data():
    """
    Scrape todos os blocos de produção do site da Embrapa para o ano informado.
    Se falhar, faz fallback para o CSV, retornando todos os dados (se year=None) ou apenas do ano (se year informado).
    Retorna uma lista de dicts: [{categoria, produto, ano, valor}] com campo 'fonte'
    """
    try:
        anos = list(range(1970, 2024))
        result = []
        for ano in anos:
            ano_data = fetch_producao_data_por_ano(ano)
            if ano_data:
                for bloco in ano_data[str(ano)]:
                    categoria = bloco['categoria']
                    for item in bloco['produtos']:
                        result.append({
                            'categoria': categoria,
                            'produto': item['produto'],
                            'ano': str(ano),
                            'valor': item['quantidade']
                        })
        return {
            "dados": result,
            "fonte": "Embrapa - Sistema de dados vitivinícolas"
        }
    except Exception:
        csv_data = load_csv_fallback(year=None, agrupado=False, csv_path=CSV_PATH_PRODUCAO)
        return {
            "dados": csv_data,
            "fonte": "Dados internos - Embrapa .csv"
        }

def fetch_producao_data_por_ano(ano):
    """
    Scraping dinâmico por ano, agrupando produtos por categoria, e fallback para CSV se scraping falhar OU se scraping retornar lista vazia.
    Retorna: {"ano": [ {"categoria": ..., "produtos": [ {"produto": ..., "quantidade": ... }, ... ] }, ... ], "fonte": "..."}
    """
    url = f"{EMBRAPA_BASE_URL}{ano}&opcao=opt_02"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find('table', {'class': 'tb_dados'})
        if not table:
            raise Exception("Tabela não encontrada")

        dados = {str(ano): []}
        categoria_atual = None
        produtos = []

        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 1 and cols[0].has_attr('colspan'):
                if categoria_atual and produtos:
                    dados[str(ano)].append({
                        "categoria": categoria_atual,
                        "produtos": produtos
                    })
                    produtos = []
                categoria_atual = cols[0].get_text(strip=True)
            elif len(cols) == 2 and categoria_atual:
                produto = cols[0].get_text(strip=True)
                valor_txt = cols[1].get_text(strip=True).replace('.', '').replace('-', '0')
                try:
                    quantidade = int(re.sub(r'\D', '', valor_txt))
                except:
                    quantidade = 0
                produtos.append({
                    "produto": produto,
                    "quantidade": quantidade
                })

        if categoria_atual and produtos:
            dados[str(ano)].append({
                "categoria": categoria_atual,
                "produtos": produtos
            })

        if not dados[str(ano)]:
            raise Exception("Scraping retornou vazio")
        
        dados["fonte"] = "Embrapa - Sistema de dados vitivinícolas"
        return dados

    except Exception:
        csv_data = load_csv_fallback(year=ano, agrupado=True, csv_path=CSV_PATH_PRODUCAO)
        if csv_data:
            csv_data["fonte"] = "Dados internos - Embrapa .csv"
        return csv_data
