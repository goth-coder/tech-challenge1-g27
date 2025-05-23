from flask import request, jsonify
from app.services.importacao_service import fetch_all, fetch_importacao_data, IMPORTACAO_SUBOPCOES


def download_importacao():
    """
    Baixa os dados de importação para todos os anos e tipos.
    """
    try:
        fetch_all()
        return jsonify({"message": "Dados de importação baixados com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_importacao_subtipo(subtipo):
    """
    Consulta dados de importação para um subtipo e anos específicos ou todos.
    """
    ano = request.args.get('ano', type=int)
    anos_range = request.args.get('anos')
 
    if anos_range:
        try:
            start, end = map(int, anos_range.split('-'))
            if start < 1970 or end > 2024:
                return jsonify({"error": "Range de anos deve ser entre 1970 e 2024"}), 400
            anos = list(range(start, end + 1))
        except ValueError:
            return jsonify({"error": "Formato de anos inválido. Use ex: 2020-2024"}), 400
    elif ano:
        if ano < 1970 or ano > 2024:
            return jsonify({"error": "Ano deve ser entre 1970 e 2024"}), 400
        anos = [ano]
    else:
        anos = list(range(1970, 2025))  # todos os anos
    
    result = []
    for a in anos:
        try:
            data = fetch_importacao_data(a, subtipo)
            # print(data)
            if data:
                result.extend(data)
        except Exception as e:
            return jsonify({"error": f"Erro ao buscar dados para {subtipo} em {a}: {str(e)}"}), 500

    if not result:
        return jsonify({"error": f"Dados não encontrados para subtipo '{subtipo}' nos anos informados"}), 404

    return jsonify({
        "subtipo": subtipo,
        "anos": anos,
        "dados": result
    }), 200