from flask import Blueprint
from app.controllers import producao_controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Produção'],
    'summary': 'Retorna todos os dados de produção de 1970 a 2023',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna todos os dados de produção de vinho de 1970 a 2023.',
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Dados de produção de vinho',
        },
        401: {
            'description': 'Token JWT ausente ou inválido'
        }
    }
})
def get_producao():
    return producao_controller.get_producao()

@producao_bp.route('/producao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Produção'],
    'summary': 'Retorna dados de produção de um ano específico',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>. Retorna dados de produção de vinho para o ano informado.',
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
            'description': 'Dados de produção de vinho do ano',
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
def get_producao_ano(ano):
    return producao_controller.get_producao_ano(ano)
