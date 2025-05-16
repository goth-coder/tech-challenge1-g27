from flask import Flask, Blueprint, jsonify

app = Flask(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({'msg': 'API Embrapa Vitivinicultura - OK'})

# Importação dos blueprints de rotas principais
# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)