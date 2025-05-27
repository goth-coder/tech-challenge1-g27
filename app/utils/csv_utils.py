import pandas as pd
import os
from app.utils.config import CSV_PATH_PRODUCAO

def load_csv_fallback(year=None, agrupado=False, csv_path=CSV_PATH_PRODUCAO):
    """
    Carrega dados do CSV de fallback para produção.
    Pode filtrar por ano e agrupar por categoria.
    """
    if not os.path.exists(csv_path):
        return None
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8', engine='python', on_bad_lines='skip')
    df = df.melt(id_vars=['produto', 'control'], var_name='ano', value_name='valor')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0).astype(int)
    df['categoria'] = df['control']

    if year:
        df = df[df['ano'] == str(year)]

    if agrupado:
        resultado = {str(year): []}
        for cat, grupo in df.groupby('categoria'):
            produtos = grupo[['produto', 'valor']].rename(columns={'valor': 'quantidade'}).to_dict(orient='records')
            resultado[str(year)].append({
                'categoria': cat,
                'produtos': produtos
            })
        return resultado
    else:
        return df[['categoria', 'produto', 'ano', 'valor']].to_dict(orient='records')
