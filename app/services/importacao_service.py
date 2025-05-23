# Serviço para scraping e fallback de importação
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import requests

def fetch_importacao_data(year=None):
    """
    Scrape todos os blocos de importação do site da Embrapa para o ano informado.
    Se falhar, faz fallback para o CSV, retornando todos os dados (se year=None) ou apenas do ano (se year informado).
    Retorna uma lista de dicts: [{categoria, produto, ano, valor}]
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year if year else 2023}&opcao=opt_05"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')  
        tables = soup.find_all('table', {'class': 'tb_dados'}) 
        if not tables:
            raise Exception("Tabela não encontrada")
        result = []
        for table in tables:
            for row in table.find_all('tr'): 
                cols = row.find_all('td') 
                row_list = [col.get_text(strip=True).replace('.', '').replace('-', '0') for col in cols]
                if row_list != []:
 
                    pais, quantidade, valor = row_list[:3]
                    print(pais, quantidade, valor)
                    
                    result.append({                    
                        'ano': str(year) if year else None,
                        'pais': pais,
                        'quantidade': float(quantidade),                    
                        'valor': float(valor)
                    })
                 
    except Exception:
        "Tries to read from CSV if scraping fails"
        csv_path = os.path.join(os.path.dirname(__file__), '../../static_data/importacao.csv')
        if not os.path.exists(csv_path):
            return None
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
        melted = df.melt(id_vars=[col for col in df.columns if col not in [str(y) for y in range(1900, 2100)]], var_name='ano', value_name='valor')
        if year:
            melted = melted[melted['ano'] == str(year)]
        melted['categoria'] = melted['control'] if 'control' in melted.columns else melted['produto']
        melted['produto'] = melted['produto']
        melted['valor'] = pd.to_numeric(melted['valor'], errors='coerce').fillna(0).astype(int)
        return melted[['categoria', 'produto', 'ano', 'valor']].to_dict(orient='records')

def fetch_importacao_data_por_ano(ano):
    """
    Scraping dinâmico por ano, agrupando produtos por categoria, igual ao HTML de referência.
    Fallback para CSV se scraping falhar OU se scraping retornar lista vazia.
    Retorna: {"ano": [ {"categoria": ..., "produtos": [ {"produto": ..., "quantidade": ... }, ... ] }, ... ] }
    """
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02"
    try:
        response = requests.get(url, timeout=10)
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
                quantidade_texto = cols[1].get_text(strip=True).replace('.', '').replace('-', '0')
                try:
                    quantidade = int(re.sub(r'\D', '', quantidade_texto))
                except ValueError:
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
        return dados
    except Exception:
        csv_path = os.path.join(os.path.dirname(__file__), '../../static_data/importacao.csv')
        if not os.path.exists(csv_path):
            return None
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
        year_col = str(ano)
        if 'control' in df.columns:
            grouped = df.groupby('control')
        else:
            grouped = df.groupby('produto')
        dados = {str(ano): []}
        for categoria, group in grouped:
            produtos = []
            for _, row in group.iterrows():
                produto = row['produto']
                try:
                    quantidade = int(row[year_col])
                except Exception:
                    quantidade = 0
                produtos.append({
                    "produto": produto,
                    "quantidade": quantidade
                })
            dados[str(ano)].append({
                "categoria": categoria,
                "produtos": produtos
            })
        return dados

def normalize_key(text):
    return re.sub(r'[^a-z0-9_]', '', text.strip().lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('â', 'a').replace('ê', 'e').replace('ô', 'o').replace('õ', 'o').replace('ü', 'u').replace('à', 'a'))

def parse_int(text):
    txt = text.strip().replace('.', '').replace('-', '0')
    try:
        return int(re.sub(r'\D', '', txt))
    except Exception:
        return 0




fetch_importacao_data(2024)
# fetch_importacao_data_por_ano(2023)