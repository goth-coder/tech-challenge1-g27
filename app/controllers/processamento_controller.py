from flask import jsonify
from app.services.processamento_service import fetch_processamento_data_por_ano, fetch_processamento_data

def get_processamento_ano(ano):
    if ano < 1970 or ano > 2023:
        return jsonify({"error": "Ano deve ser entre 1970 e 2023"}), 400
    dados = fetch_processamento_data_por_ano(ano)
    if not dados or not str(ano) in dados:
        return jsonify({"error": f"Dados para o ano {ano} não encontrados"}), 404
    return jsonify(dados)

def get_processamento_tipo_ano(tipo, ano):
    if ano < 1970 or ano > 2023:
        return jsonify({"error": "Ano deve ser entre 1970 e 2023"}), 400
    dados = fetch_processamento_data(ano, tipo)
    if not dados:
        return jsonify({"error": f"Dados para o tipo {tipo} no ano {ano} não encontrados"}), 404
    return jsonify({"ano": ano, "tipo": tipo, "dados": dados})
