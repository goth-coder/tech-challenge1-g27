from flask import Blueprint
from app.controllers import exportacao_controller as controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Faz o download de todos os dados de Exportação de 1970 a 2024',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna todos os dados de Exportação de vinho de 1970 a 2024.',
    'parameters': [
        {
            'name': 'ano',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Ano desejado (1970-2024)'
        }
    ],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': '✅ Dados de Exportação baixados com sucesso',
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def get_ano(ano):
    return controller.get_ano(ano)

@exportacao_bp.route('/exportacao/<string:tipo>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Retorna dados de Exportação de um tipo específico e anos informados',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna dados de Exportação para o subtipo, podendo filtrar anos com query param "ano" ou "anos".',
    'parameters': [
        {
            'name': 'subtipo',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Subtipo desejado (ex: Vinhos de mesa, Espumantes...)'
        },
        {
            'name': 'anos',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Range de anos desejados, separados por traço. Exemplo: 2020-2024'
        },    
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano único desejado (1970-2024)'
        }
    ],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Query de dados de Exportação bem sucedida',
        },
        400: {
            'description': 'Ano inválido'
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        },
        404: {
            'description': 'Dados não encontrados'
        }
    }
})
def get_tipo_ano(tipo):
    return controller.get_tipo_ano(tipo)

# Rotas
## Para fazer download dos dados de Exportação
## Query de acordo com o tipo contendo todos os anos
## Query de acordo com o tipo e ano
