import os
import pandas as pd
import csv
from app.utils.config import (
    CSV_PATH_EXPORTACAO_VINHOS,
    CSV_PATH_EXPORTACAO_ESPUMANTES,
    CSV_PATH_EXPORTACAO_FRESCAS,
    CSV_PATH_EXPORTACAO_SUCO
)

CSV_MAP = {
    'vinhos': CSV_PATH_EXPORTACAO_VINHOS,
    'espumantes': CSV_PATH_EXPORTACAO_ESPUMANTES,
    'frescas': CSV_PATH_EXPORTACAO_FRESCAS,
    'suco': CSV_PATH_EXPORTACAO_SUCO,
}

def load_exportacao_csv(tipo, ano):
    """
    Carrega dados do CSV de fallback para o tipo e ano de exportação.
    Tenta detectar delimitador, mas faz fallback manual para tab e ponto e vírgula.
    Retorna [{'pais': ..., 'quantidade': ..., 'valor': ...}] para o ano solicitado.
    """
    path = CSV_MAP.get(tipo)
    if not path or not os.path.exists(path):
        return []
    
    delimiters = ['\t', ';', ',']
    delimiter = None
    
    # Tenta detectar delimitador automaticamente
    try:
        with open(path, 'r', encoding='utf-8') as f:
            sample = f.read(2048)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
    except Exception:
        for delim in delimiters:
            try:
                df = pd.read_csv(path, sep=delim, encoding='utf-8', engine='python', on_bad_lines='skip')
                if df.shape[1] > 2:
                    delimiter = delim
                    break
            except Exception:
                continue
    
    if not delimiter:
        try:
            df = pd.read_csv(path, sep='\t', encoding='utf-8', engine='python', on_bad_lines='skip')
            delimiter = '\t'
        except Exception:
            return []
    
    if delimiter:
        df = pd.read_csv(path, sep=delimiter, encoding='utf-8', engine='python', on_bad_lines='skip')
    
    ano_str = str(ano)
    
    # Normaliza nomes de colunas
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Procura coluna país
    pais_col = None
    for col in df.columns:
        if 'país' in col or 'pais' in col:
            pais_col = col
            break
    
    if not pais_col:
        return []
    
    # Verifica se existem colunas para o ano (quantidade e valor)
    # O CSV tem formato: País, ano_quantidade, ano_valor, ...
    # As colunas se repetem: 1970, 1970, 1971, 1971, etc.
    
    result = []
    columns = df.columns.tolist()
    
    # Procura pelas colunas do ano específico
    ano_indices = []
    for i, col in enumerate(columns):
        if col == ano_str:
            ano_indices.append(i)
    
    if len(ano_indices) < 2:
        return []
    
    # Assume que a primeira ocorrência é quantidade e segunda é valor
    quantidade_col = columns[ano_indices[0]]
    valor_col = columns[ano_indices[1]]
    
    for _, row in df.iterrows():
        quantidade = row.iloc[ano_indices[0]]
        valor = row.iloc[ano_indices[1]]
        
        # Limpa valores
        if isinstance(quantidade, str):
            quantidade = quantidade.strip()
            if quantidade.lower() in ['nd', '*', '', '-']:
                quantidade = 0
        
        if isinstance(valor, str):
            valor = valor.strip()
            if valor.lower() in ['nd', '*', '', '-']:
                valor = 0
        
        try:
            quantidade = int(quantidade) if quantidade else 0
        except:
            quantidade = 0
            
        try:
            valor = int(valor) if valor else 0
        except:
            valor = 0
        
        result.append({
            'pais': row[pais_col],
            'quantidade': quantidade,
            'valor': valor
        })
    
    return result
