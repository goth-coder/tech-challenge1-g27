import os
import pandas as pd
from app.utils.config import (
    CSV_PATH_PROCESSAMENTO_VINIFERAS,
    CSV_PATH_PROCESSAMENTO_AMERICANAS,
    CSV_PATH_PROCESSAMENTO_MESA,
    CSV_PATH_PROCESSAMENTO_SEMCLASS
)

CSV_MAP = {
    'viniferas': CSV_PATH_PROCESSAMENTO_VINIFERAS,
    'americanas': CSV_PATH_PROCESSAMENTO_AMERICANAS,
    'mesa': CSV_PATH_PROCESSAMENTO_MESA,
    'semclass': CSV_PATH_PROCESSAMENTO_SEMCLASS,
}

def load_processamento_csv(tipo, ano):
    """
    Carrega dados do CSV de fallback para o tipo e ano.
    Tenta detectar delimitador, mas faz fallback manual para tab e ponto e vírgula.
    Retorna [{'produto': ..., 'quantidade': ...}] para o ano solicitado.
    """
    import csv
    path = CSV_MAP.get(tipo)
    if not path or not os.path.exists(path):
        return []
    delimiters = ['\t', ';']
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
    # Procura coluna cultivar
    cultivar_col = None
    for col in df.columns:
        if 'cultivar' in col:
            cultivar_col = col
            break
    if not cultivar_col or ano_str not in df.columns:
        return []
    result = []
    for _, row in df.iterrows():
        valor = row[ano_str]
        if isinstance(valor, str):
            valor = valor.strip()
            if valor.lower() in ['nd', '*', '']:
                valor = None
        result.append({'produto': row[cultivar_col], 'quantidade': valor})
    return result