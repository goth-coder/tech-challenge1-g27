from flask import Blueprint
from app.controllers import importacao_controller as controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Retorna dados de importacao de todas as subopções para o ano informado',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>.',
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
            'description': '✅ Dados de Importação obtidos com sucesso',
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def get_ano(ano):
    return controller.get_ano(ano)


@importacao_bp.route('/importacao/<string:tipo>/', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Retorna dados de Importação de um tipo específico e anos informados',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna dados de Importação para o subtipo, podendo filtrar anos com query param "ano" ou "anos".',
    'parameters': [
        {
            'name': 'tipo',
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
def get_tipo_ano(tipo):
    return controller.get_tipo_ano(tipo)
