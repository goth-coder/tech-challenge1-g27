from flask import jsonify
from app.services.comercializacao_service import fetch_comercializacao_data_por_ano

def get_comercializacao():
    anos = list(range(1970, 2024))
    dados = {}
    for ano in anos:
        ano_data = fetch_comercializacao_data_por_ano(ano)
        if ano_data and str(ano) in ano_data and ano_data[str(ano)]:
            dados[str(ano)] = ano_data[str(ano)]
    return jsonify({"anos": dados})

def get_comercializacao_ano(ano):
    if ano < 1970 or ano > 2023:
        return jsonify({"error": "Ano deve ser entre 1970 e 2023"}), 400
    dados = fetch_comercializacao_data_por_ano(ano)
    if not dados or not str(ano) in dados or not dados[str(ano)]:
        return jsonify({"error": f"Dados para o ano {ano} não encontrados", "debug": dados}), 404
    return jsonify(dados)
