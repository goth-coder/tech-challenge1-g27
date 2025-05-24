from flask import Blueprint
from app.controllers import comercializacao_controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

comercializacao_bp = Blueprint('comercializacao', __name__)

@comercializacao_bp.route('/comercializacao', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Comercialização'],
    'summary': 'Retorna todos os dados de comercialização de 1970 a 2023',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna todos os dados de comercialização de vinho de 1970 a 2023.',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Dados de comercialização de vinhos e derivados',
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def get_comercializacao():
    return comercializacao_controller.get_comercializacao()

@comercializacao_bp.route('/comercializacao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Comercialização'],
    'summary': 'Retorna dados de comercialização de um ano específico',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna dados de comercialização de vinho para o ano informado.',
    'parameters': [
        {
            'name': 'ano',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Ano desejado (1970-2023)'
        }
    ],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Dados de comercialização de vinho do ano',
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
def get_comercializacao_ano(ano):
    return comercializacao_controller.get_comercializacao_ano(ano)
