# app/controllers/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.auth.auth_utils import hash_password, verify_password
from app.auth.jwt_manager import jwt

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'Usuário e senha obrigatórios'}), 400
    if User.find_by_username(username):
        return jsonify({'msg': 'Usuário já existe'}), 409
    User.register(username, password)
    return jsonify({'msg': 'Usuário registrado com sucesso'}), 201

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'Usuário e senha obrigatórios'}), 400
    user = User.find_by_username(username)
    #if user is None:
        #return jsonify({'msg': 'Usuário não registrado'}), 404
    if user is None or not user.verify_password(password):
        return jsonify({'msg': 'Usuário ou senha incorretos'}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200
