import pandas as pd
import os 
import csv
import logging
import unicodedata

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


# Logging clean
logging.basicConfig(level=logging.DEBUG, format='[CSV] %(message)s')
logger = logging.getLogger(__name__)

def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

def load_generic_csv(tipo, ano, csv_map, id_col_name, value_col_name=None, output_keys=None):
    logger.debug(f"Tipo: {tipo}, Ano: {ano}")
    path = csv_map.get(tipo)
    logger.debug(f"Resolved CSV path: {path}")
    if not path or not os.path.exists(path):
        logger.warning(f"Path not found: {path}")
        return []

    delimiters = ['\t', ';', ',']
    delimiter = None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            sample = f.read(2048)
            delimiter = csv.Sniffer().sniff(sample).delimiter
            # logger.debug(f"Detected delimiter: {repr(delimiter)}")
    except Exception as e:
        # logger.warning(f"csv.Sniffer failed: {e}")
        for delim in delimiters:
            try:
                df = pd.read_csv(path, sep=delim, encoding='utf-8', engine='python', on_bad_lines='skip')
                if df.shape[1] > 2:
                    delimiter = delim
                    # logger.debug(f"Fallback delimiter selected: {repr(delim)}")
                    break
            except Exception:
                continue

    if not delimiter:
        delimiter = '\t'
        # logger.debug("Defaulting to tab delimiter")

    df = pd.read_csv(path, sep=delimiter, encoding='utf-8', engine='python', on_bad_lines='skip')
    df.columns = [col.strip().lower() for col in df.columns] 

    ano_str = str(ano)
    id_col_norm = normalize_text(id_col_name)
    id_col = None
    for col in df.columns:
        if normalize_text(col) == id_col_norm:
            id_col = col
            break

    if not id_col:
        logger.warning(f"id_col_name '{id_col_name}' not found")
        return []

    if value_col_name is None:
        if ano_str not in df.columns:
            logger.warning(f"Ano column '{ano_str}' not found")
            return []
        result = []
        for _, row in df.iterrows():
            valor = row[ano_str]
            if isinstance(valor, str):
                valor = valor.strip()
                if valor.lower() in ['nd', '*', '', '-']:
                    valor = None
            item = {
                output_keys.get('id', 'id'): row[id_col],
                output_keys.get('qtd', 'quantidade'): valor
            }
            result.append(item)
        return result

    else:
        columns = df.columns.tolist()
        ano_indices = [i for i, col in enumerate(columns) if col == ano_str]
        # logger.debug(f"Found columns for ano '{ano_str}': {ano_indices}")

        result = []
        if len(ano_indices) == 1:
            # logger.warning(f"Only one column found for '{ano_str}', assuming it's 'quantidade'")
            for _, row in df.iterrows():
                quantidade = row.iloc[ano_indices[0]]
                if isinstance(quantidade, str):
                    quantidade = quantidade.strip()
                    if quantidade.lower() in ['nd', '*', '', '-']:
                        quantidade = 0
                try:
                    quantidade = int(quantidade) if quantidade else 0
                except:
                    quantidade = 0
                item = {
                    output_keys.get('id', 'id'): row[id_col],
                    output_keys.get('qtd', 'quantidade'): quantidade,
                    output_keys.get('val', 'valor'): 0
                }
                result.append(item)
        elif len(ano_indices) >= 2:
            for _, row in df.iterrows():
                quantidade = row.iloc[ano_indices[0]]
                valor = row.iloc[ano_indices[1]]
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
                item = {
                    output_keys.get('id', 'id'): row[id_col],
                    output_keys.get('qtd', 'quantidade'): quantidade,
                    output_keys.get('val', 'valor'): valor
                }
                result.append(item)
        else:
            logger.warning(f"No column for '{ano_str}' found")
        return result
