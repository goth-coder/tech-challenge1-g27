from flask import jsonify
from app.services.comercializacao_service import fetch_comercializacao_data_por_ano, fetch_comercializacao_data

def get_comercializacao():
    # Para todos os anos, usar o service que já retorna os dados com fonte
    data_with_source = fetch_comercializacao_data()
    return jsonify(data_with_source)

def get_comercializacao_ano(ano):
    if ano < 1970 or ano > 2023:
        return jsonify({"error": "Ano deve ser entre 1970 e 2023"}), 400
    dados = fetch_comercializacao_data_por_ano(ano)
    if not dados or not str(ano) in dados or not dados[str(ano)]:
        return jsonify({"error": f"Dados para o ano {ano} não encontrados"}), 404
    return jsonify(dados)
