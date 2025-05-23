import re

def normalize_key(text):
    """
    Remove acentos, espaços e caracteres especiais, deixando apenas letras minúsculas, números e underscores.
    """
    return re.sub(r'[^a-z0-9_]', '', text.strip().lower().replace(' ', '_')
        .replace('ç', 'c').replace('ã', 'a').replace('á', 'a')
        .replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        .replace('â', 'a').replace('ê', 'e').replace('ô', 'o').replace('õ', 'o')
        .replace('ü', 'u').replace('à', 'a'))

def parse_int(text):
    """
    Converte texto para inteiro, removendo pontos e tratando traços como zero.
    Retorna 0 em caso de erro.
    """
    txt = text.strip().replace('.', '').replace('-', '0')
    try:
        return int(re.sub(r'\D', '', txt))
    except Exception:
        return 0