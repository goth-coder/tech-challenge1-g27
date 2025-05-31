# Rotas para importação
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.controllers.importacao_controller import get_importacao_ano, get_importacao_tipo_ano

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Dados de importação por ano',
    'description': 'Retorna dados de todas as subopções de importação para o ano informado',
    'parameters': [
        {
            'name': 'ano',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Ano dos dados (1970-2024)'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de importação encontrados',
            'schema': {
                'type': 'object',
                'properties': {
                    'ano': {'type': 'integer'},
                    'dados': {
                        'type': 'object',
                        'properties': {
                            'vinhos': {'type': 'array'},
                            'espumantes': {'type': 'array'},
                            'frescas': {'type': 'array'},
                            'passas': {'type': 'array'},
                            'suco': {'type': 'array'}
                        }
                    },
                    'fonte': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Ano inválido'},
        404: {'description': 'Dados não encontrados'},
        500: {'description': 'Erro interno do servidor'}
    },
    'security': [{'BearerAuth': []}]
})
def importacao_ano(ano):
    """Endpoint para buscar dados de importação por ano"""
    return get_importacao_ano(ano)

@importacao_bp.route('/importacao/<string:tipo>/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Importação'],
    'summary': 'Dados de importação por tipo e ano',
    'description': 'Retorna dados de uma subopção específica de importação para o ano',
    'parameters': [
        {
            'name': 'tipo',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Tipo de importação: vinhos, espumantes, frescas, passas, suco'
        },
        {
            'name': 'ano',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Ano dos dados (1970-2024)'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de importação encontrados',
            'schema': {
                'type': 'object',
                'properties': {
                    'ano': {'type': 'integer'},
                    'tipo': {'type': 'string'},
                    'dados': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'pais': {'type': 'string'},
                                'quantidade': {'type': 'integer'},
                                'valor': {'type': 'integer'}
                            }
                        }
                    },
                    'fonte': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Parâmetros inválidos'},
        404: {'description': 'Dados não encontrados'},
        500: {'description': 'Erro interno do servidor'}
    },
    'security': [{'BearerAuth': []}]
})
def importacao_tipo_ano(tipo, ano):
    """Endpoint para buscar dados de importação por tipo e ano"""
    return get_importacao_tipo_ano(tipo, ano)
