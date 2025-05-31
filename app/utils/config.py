import os
from dotenv import load_dotenv

load_dotenv()

EMBRAPA_BASE_URL = os.getenv("EMBRAPA_BASE_URL", "http://vitibrasil.cnpuv.embrapa.br/index.php?ano=")

CSV_PATH_PRODUCAO = os.path.join(os.path.dirname(__file__), '../../static_data/producao.csv')
CSV_PATH_COMERCIALIZACAO = os.path.join(os.path.dirname(__file__), '../../static_data/comercializacao.csv')
STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../static_data')
CSV_PATH_PROCESSAMENTO_VINIFERAS = os.path.join(STATIC_DATA_PATH, 'processamentoViniferas.csv')
CSV_PATH_PROCESSAMENTO_AMERICANAS = os.path.join(STATIC_DATA_PATH, 'processamentoAmericanas.csv')
CSV_PATH_PROCESSAMENTO_MESA = os.path.join(STATIC_DATA_PATH, 'processamentoMesa.csv')
CSV_PATH_PROCESSAMENTO_SEMCLASS = os.path.join(STATIC_DATA_PATH, 'processamentoSemclass.csv')

