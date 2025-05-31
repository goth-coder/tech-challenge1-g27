# Rotas para exportação
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.controllers.exportacao_controller import get_exportacao_ano, get_exportacao_tipo_ano

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Dados de exportação por ano',
    'description': 'Retorna dados de todas as subopções de exportação para o ano informado',
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
            'description': 'Dados de exportação encontrados',
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
def exportacao_ano(ano):
    """Endpoint para buscar dados de exportação por ano"""
    return get_exportacao_ano(ano)

@exportacao_bp.route('/exportacao/<string:tipo>/<int:ano>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Exportação'],
    'summary': 'Dados de exportação por tipo e ano',
    'description': 'Retorna dados de uma subopção específica de exportação para o ano',
    'parameters': [
        {
            'name': 'tipo',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Tipo de exportação: vinhos, espumantes, frescas, suco'
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
            'description': 'Dados de exportação encontrados',
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
def exportacao_tipo_ano(tipo, ano):
    """Endpoint para buscar dados de exportação por tipo e ano"""
    return get_exportacao_tipo_ano(tipo, ano)
