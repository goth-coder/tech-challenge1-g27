from flask import jsonify
from app.services.exportacao_service import fetch_exportacao_data_por_ano, fetch_exportacao_data

def get_exportacao_ano(ano):
    """
    Controller para retornar dados de todas as subopções de exportação para um ano específico.
    """
    if ano < 1970 or ano > 2024:
        return jsonify({'error': 'Ano deve estar entre 1970 e 2024'}), 400
    
    try:
        data = fetch_exportacao_data_por_ano(ano)
        if not data or not data.get(str(ano)):
            return jsonify({'error': 'Dados não encontrados para o ano informado'}), 404
        
        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

def get_exportacao_tipo_ano(tipo, ano):
    """
    Controller para retornar dados de uma subopção específica de exportação para um ano.
    """
    if ano < 1970 or ano > 2024:
        return jsonify({'error': 'Ano deve estar entre 1970 e 2024'}), 400
    
    tipos_validos = ['vinhos', 'espumantes', 'frescas', 'suco']
    if tipo not in tipos_validos:
        return jsonify({
            'error': f'Tipo de exportação inválido. Tipos válidos: {", ".join(tipos_validos)}'
        }), 400
    
    try:
        data = fetch_exportacao_data(ano, tipo)
        if not data:
            return jsonify({'error': 'Dados não encontrados para o tipo e ano informados'}), 404
        
        return jsonify({
            'ano': ano,
            'tipo': tipo,
            'dados': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500
