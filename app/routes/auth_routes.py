# app/routes/auth_routes.py
from flask import Blueprint
from app.controllers import auth_controller
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Cadastro de novo usuário',
    'description': 'Cria um novo usuário e retorna mensagem de sucesso.\n\nExemplo de uso via curl:\n\n    curl -X POST "http://localhost:5001/register" -H "Content-Type: application/json" -d "{\"username\": \"usuario\", \"password\": \"senha\"}"',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string'},
                        'password': {'type': 'string'}
                    },
                    'required': ['username', 'password']
                },
                'example': {
                    'username': 'usuario',
                    'password': 'senha'
                }
            }
        }
    },
    'security': [],
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'content': {
                'application/json': {
                    'example': {'msg': 'Usuário registrado com sucesso'}
                }
            }
        },
        400: {
            'description': 'Usuário já existe',
            'content': {
                'application/json': {
                    'example': {'msg': 'Usuário já existe'}
                }
            }
        }
    }
})
def register():
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login do usuário',
    'description': 'Realiza login e retorna o token JWT.\n\nExemplo de uso via curl:\n\n    curl -X POST "http://localhost:5001/login" -H "Content-Type: application/json" -d "{\"username\": \"usuario\", \"password\": \"senha\"}"',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'username': {'type': 'string'},
                        'password': {'type': 'string'}
                    },
                    'required': ['username', 'password']
                },
                'example': {
                    'username': 'usuario',
                    'password': 'senha'
                }
            }
        }
    },
    'security': [],
    'responses': {
        200: {
            'description': 'Login realizado com sucesso',
            'content': {
                'application/json': {
                    'example': {'access_token': 'jwt_token'}
                }
            }
        },
        401: {
            'description': 'Credenciais inválidas',
            'content': {
                'application/json': {
                    'example': {'msg': 'Usuário ou senha inválidos'}
                }
            }
        }
    }
})
def login():
    return auth_controller.login()