from flask import request, jsonify
from app.services.importacao_service import fetch_importacao_data_por_ano, fetch_importacao_data


def get_ano(ano):
    """
    Retrieve import data for a specific year.
    Args:
        ano (int): The year for which to retrieve import data. Must be between 1970 and 2024.
    Returns:
        Response: A Flask JSON response containing:
            The import data for the specified year (HTTP 200), if found.
            An error message (HTTP 400) if the year is out of the allowed range.
            An error message (HTTP 404) if no data is found for the specified year.
    Example:
        response = get_importacao_ano(2020)
    """
    if ano < 1970 or ano > 2024:
        return jsonify({"error": "Ano deve ser entre 1970 e 2024"}), 400
    dados = fetch_importacao_data_por_ano(ano)
    if not dados or not str(ano) in dados:
        return jsonify({"error": f"Dados para o ano {ano} não encontrados"}), 404
    return jsonify(dados)


def get_tipo_ano(tipo):
    """
    Consulta e retorna dados de importação para um determinado tipo e intervalo de anos.
    Parâmetros:
        tipo (str): O tipo de importação a ser consultado.

    Query Parameters:
        ano (int, opcional): Ano específico para consulta (entre 1970 e 2024).
        anos (str, opcional): Intervalo de anos no formato 'YYYY-YYYY' (ex: '2020-2024').

    Regras:
        Se 'anos' for informado, será considerado o intervalo especificado.
        Se apenas 'ano' for informado, será considerado apenas esse ano.
        Se nenhum for informado, serão considerados todos os anos de 1970 a 2024.
        Os anos devem estar no intervalo de 1970 a 2024.

    Retornos:
        200: Dados de importação encontrados, no formato JSON contendo tipo, anos e dados.
        400: Erro de validação nos parâmetros (ano(s) fora do intervalo ou formato inválido).
        404: Nenhum dado encontrado para o tipo e anos informados.
        500: Erro interno ao buscar dados.

    Exemplo de resposta bem-sucedida:
        {
            "tipo": "exemplo",
            "anos": [2020, 2021],
            "dados": [...]
        }
    Consulta dados de importação para um tipo e anos específicos ou todos.
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
    for ano in anos:
        try:
            data = fetch_importacao_data(ano, tipo)
            if data:
                result.extend(data)
        except Exception as e:
            return jsonify({"error": f"Erro ao buscar dados para {tipo} em {ano}: {str(e)}"}), 500

    if not result:
        return jsonify({"error": f"Dados não encontrados para tipo '{tipo}' nos anos informados"}), 404

    return jsonify({
        "tipo": tipo,
        "anos": anos,
        "dados": result
    }), 200