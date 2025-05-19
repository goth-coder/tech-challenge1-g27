from flask import Blueprint
from app.controllers import processamento_controller
from flask_jwt_extended import jwt_required
from flasgger import swag_from

processamento_bp = Blueprint('processamento', __name__)

@processamento_bp.route('/processamento/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Processamento'],
    'summary': 'Retorna dados de processamento de todas as subopções para o ano informado',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>.',
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
        200: {'description': 'Dados de processamento do ano'},
        400: {'description': 'Ano inválido'},
        401: {'description': 'Token JWT ausente ou inválido'},
        404: {'description': 'Dados não encontrados'}
    }
})
def get_processamento_ano(ano):
    return processamento_controller.get_processamento_ano(ano)

@processamento_bp.route('/processamento/<string:tipo>/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Processamento'],
    'summary': 'Retorna dados de processamento de uma subopção específica para o ano informado',
    'description': 'Requer autenticação JWT. Envie o token no header Authorization: Bearer <token>.',
    'parameters': [
        {'name': 'tipo', 'in': 'path', 'type': 'string', 'required': True, 'description': 'viniferas, americanas, mesa, semclass'},
        {'name': 'ano', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Ano desejado (1970-2023)'}
    ],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {'description': 'Dados de processamento do tipo e ano'},
        400: {'description': 'Ano inválido'},
        401: {'description': 'Token JWT ausente ou inválido'},
        404: {'description': 'Dados não encontrados'}
    }
})
def get_processamento_tipo_ano(tipo, ano):
    return processamento_controller.get_processamento_tipo_ano(tipo, ano)
