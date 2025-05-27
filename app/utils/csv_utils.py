import pandas as pd
import os

def load_csv_fallback(year=None, agrupado=False, csv_path=None):
    """
    Carrega dados do CSV de fallback para a categoria em questão.
    Parâmetros:
        year: ano a filtrar (opcional)
        agrupado: se True, agrupa por categoria
        csv_path: caminho do CSV (obrigatório)
    """
    if not csv_path or not os.path.exists(csv_path):
        print("Arquivo .csv não existe")
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
