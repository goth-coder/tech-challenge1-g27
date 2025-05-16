# app/models/user.py
# Modelo simples de usuário (armazenamento em memória para exemplo)

from app.auth.auth_utils import hash_password, verify_password

class User:
    users = {}

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    @classmethod
    def find_by_username(cls, username):
        return cls.users.get(username)

    @classmethod
    def register(cls, username, password):
        if username in cls.users:
            return None
        password_hash = hash_password(password)
        user = User(username, password_hash)
        cls.users[username] = user
        return user

    def verify_password(self, password):
        return verify_password(password, self.password_hash)
