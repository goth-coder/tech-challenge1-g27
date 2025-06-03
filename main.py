from flask import Flask
from flasgger import Swagger
from app.routes.auth_routes import auth_bp
from app.auth.jwt_manager import jwt
from app.routes.main_routes import main_bp
from app.routes.producao_routes import producao_bp
from app.routes.processamento_routes import processamento_bp
from app.routes.comercializacao_routes import comercializacao_bp
from app.routes.importacao_routes import importacao_bp
from app.routes.exportacao_routes import exportacao_bp
from app.utils.swagger_config import SWAGGER_CONFIG
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = SWAGGER_CONFIG
    Swagger(app, template=app.config['SWAGGER'])
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(producao_bp)
    app.register_blueprint(processamento_bp)
    app.register_blueprint(comercializacao_bp)
    app.register_blueprint(importacao_bp)
    app.register_blueprint(exportacao_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)