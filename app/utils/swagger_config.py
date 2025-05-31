"""Configurações do Swagger"""
SWAGGER_CONFIG = {
    'openapi': '3.0.2',
    'info': {
        'title': 'API Embrapa Vitivinicultura',
        'description': 'API para consulta de dados de vitivinicultura',
        'version': '1.0.0'
    },
    'components': {
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'
            }
        }
    },
    'security': [{'BearerAuth': []}],
    'specs_route': '/apidocs/',
    'tags': [
        {
            'name': 'Autenticação',
            'description': 'Endpoints para autenticação e registro de usuários'
        },
        {
            'name': 'Produção',
            'description': 'Endpoints para dados de produção de uvas'
        },
        {
            'name': 'Processamento',
            'description': 'Endpoints para dados de processamento de uvas'
        },
        {
            'name': 'Comercialização',
            'description': 'Endpoints para dados de comercialização'
        },
        {
            'name': 'Importação',
            'description': 'Endpoints para dados de importação'
        },
        {
            'name': 'Exportação',
            'description': 'Endpoints para dados de exportação'
        }
    ]
}
