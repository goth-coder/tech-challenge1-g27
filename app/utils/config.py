import os
from dotenv import load_dotenv

load_dotenv()

EMBRAPA_BASE_URL = os.getenv("EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=")

CSV_PATH_PRODUCAO = os.path.join(os.path.dirname(__file__), '../../static_data/producao.csv')
