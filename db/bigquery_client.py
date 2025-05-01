import os
from google.cloud import bigquery
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  

PROJECT_ID = os.getenv("BIGQUERY_PROJECT")
DATASET_ID = os.getenv("BIGQUERY_DATASET")
TABLE_ID = "file_metadata"

def log_file_metadata_to_bigquery(filename: str, url: str, file_type: str = None, status: str = "success"):
    client = bigquery.Client()
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    row = {
        "filename": filename,
        "url": url,
        "downloaded_at": datetime.utcnow().isoformat(),
        "file_type": file_type,
        "status": status
    }
    errors = client.insert_rows_json(table_ref, [row])
    if errors:
        raise RuntimeError(f"BigQuery insertion failed: {errors}")
