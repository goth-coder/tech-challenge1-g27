from flask import jsonify
from app.services.importacao_service import fetch_importacao_data_por_ano, fetch_importacao_data

def get_importacao_ano(ano):
    """
    Controller para retornar dados de todas as subopções de importação para um ano específico.
    """
    if ano < 1970 or ano > 2024:
        return jsonify({'error': 'Ano deve estar entre 1970 e 2024'}), 400
    
    try:
        data = fetch_importacao_data_por_ano(ano)
        if not data or not data.get(str(ano)):
            return jsonify({'error': 'Dados não encontrados para o ano informado'}), 404
        
        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

def get_importacao_tipo_ano(tipo, ano):
    """
    Controller para retornar dados de uma subopção específica de importação para um ano.
    """
    if ano < 1970 or ano > 2024:
        return jsonify({'error': 'Ano deve estar entre 1970 e 2024'}), 400
    
    tipos_validos = ['vinhos', 'espumantes', 'frescas', 'passas', 'suco']
    if tipo not in tipos_validos:
        return jsonify({
            'error': f'Tipo de importação inválido. Tipos válidos: {", ".join(tipos_validos)}'
        }), 400
    
    try:
        data_with_source = fetch_importacao_data(ano, tipo)
        if not data_with_source or not data_with_source.get("dados"):
            return jsonify({'error': 'Dados não encontrados para o tipo e ano informados'}), 404
        
        return jsonify({
            'ano': ano, 
            'tipo': tipo, 
            'dados': data_with_source["dados"],
            'fonte': data_with_source["fonte"]
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500
