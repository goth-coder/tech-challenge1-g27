from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.routes.auth_routes import auth_bp
from app.auth.jwt_manager import jwt
from app.routes.main_routes import main_bp
from app.routes.producao_routes import producao_bp
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'API Embrapa Vitivinicultura',
        'uiversion': 3,
        'openapi': '3.0.2',
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
        'specs_route': '/apidocs/'
    }
    Swagger(app, template=app.config['SWAGGER'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(producao_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)