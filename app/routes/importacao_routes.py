from flask import Blueprint
from app.controllers import importacao_controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/download', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Faz o download de todos os dados de Importação de 1970 a 2024',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna todos os dados de Importação de vinho de 1970 a 2024.',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Dados de Importação baixados com sucesso',
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def download_importacao():
    return importacao_controller.download_importacao()


@importacao_bp.route('/importacao/<subtipo>/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Retorna dados de Importação de um tipo específico e anos informados',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna dados de Importação para o subtipo, podendo filtrar anos com query param "ano" ou "anos".',
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
            'description': 'Query de dados de importação bem sucedida',
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
def get_importacao_subtipo(subtipo):
    return importacao_controller.get_importacao_subtipo(subtipo)

# Rotas
## Para fazer download dos dados de importação
## Query de acordo com o tipo contendo todos os anos
## Query de acordo com o tipo e ano
