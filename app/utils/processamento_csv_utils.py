import os
import pandas as pd
from app.utils.config import STATIC_DATA_PATH
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
    """
    path = CSV_MAP.get(tipo)
    if not path or not os.path.exists(path):
        return []
    df = pd.read_csv(path, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
    df = df[df['ano'] == int(ano)]
    return df[['cultivar', 'quantidade']].to_dict(orient='records')
