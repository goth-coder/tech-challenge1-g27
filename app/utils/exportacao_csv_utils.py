import os 
import pandas as pd
from app.utils.config import STATIC_DATA_PATH
import logging
from app.utils.config import (
    CSV_PATH_EXPORTACAO_VINHOSMESA,
    CSV_PATH_EXPORTACAO_ESPUMANTES,
    CSV_PATH_EXPORTACAO_UVASFRESCAS,
    CSV_PATH_EXPORTACAO_UVASPASSAS,
    CSV_PATH_EXPORTACAO_SUCO,
)

CSV_MAP = {
    'Vinhos de mesa': CSV_PATH_EXPORTACAO_VINHOSMESA,
    'Espumantes': CSV_PATH_EXPORTACAO_ESPUMANTES,
    'Uvas frescas': CSV_PATH_EXPORTACAO_UVASFRESCAS,
    'Uvas passas': CSV_PATH_EXPORTACAO_UVASPASSAS,
    'Suco de uva': CSV_PATH_EXPORTACAO_SUCO,
}


def save_exportacao_csv(data, tipo):
    """
    Salva a lista de dicts de produção em um arquivo CSV.
    
    Args:
        data (list): Lista de dicts [{categoria, produto, ano, valor}, ...]
        path (str): Caminho para salvar o arquivo.
    """
    path = CSV_MAP.get(tipo) 

    df = pd.DataFrame(data) 
    if os.path.exists(path):
        logging.warning(f"Arquivo CSV para o tipo '{tipo}' já existe em '{path}'. Não será sobrescrito.")
        return df
    os.makedirs(os.path.dirname(path), exist_ok=True) 
    df.to_csv(path, sep=';', index=False, encoding='utf-8')
    print(f"Arquivo salvo em: {path}")
    return df


def load_exportacao_csv(ano, tipo):
    """
    Carrega dados do CSV de fallback para o tipo e ano.
    """  
    path = CSV_MAP.get(tipo)
    if not path or not os.path.exists(path):
        logging.warning(
            "⚠️ Arquivo CSV não encontrado!\n"
            "Tipo: %s\n"
            "Path: %s\n"
            "CSV_MAP Keys: %s\n",
            tipo,
            path if path else 'Path não definido',
            list(CSV_MAP.keys())
        ) 
        return []
    df = pd.read_csv(path, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
    df = df[df['ano'] == int(ano)]
    return df.to_dict(orient='records')
