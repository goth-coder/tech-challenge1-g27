import os 
from fastapi import FastAPI
from scraper.download import download_all_files
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException 
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv() 
app = FastAPI()
 
@app.get("/")
def root():
    return {"message": "EMBRAPA Data Downloader API"}

@app.post("/download")
async def trigger_download():
    """
    Handles the POST request to trigger the download of all files.

    Returns:
        dict: A dictionary containing the status of the download operation.
    """

    result = await download_all_files()
    return {"status": result}

@app.get("/files")
def list_files():
    """
    Lists all files in the 'embrapa_files' directory.

    This function attempts to retrieve a list of all files located in the 
    'embrapa_files' directory. If the directory does not exist, it gracefully 
    handles the FileNotFoundError and returns an empty list.

    Returns:
        dict: A dictionary containing a single key 'files', which maps to a 
        list of filenames in the 'embrapa_files' directory. If the directory 
        is not found, the list will be empty.
    """
    "Lists files in the local directory"
    try:
        files = os.listdir("embrapa_files")
        return {"files": files}
    except FileNotFoundError:
        return {"files": []}
    
    
@app.get("/preview/{filename}")
def get_file(filename: str):
    """
    Fetches a file from the 'embrapa_files' directory.

    Args:
        filename (str): The name of the file to retrieve.

    Returns:
        FileResponse: The file response object if the file exists.

    Raises:
        HTTPException: If the file is not found.
    """
    file_path = os.path.join("embrapa_files", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path)


@app.get("/health")
async def health_check():
    """
    Performs a health check by executing a simple query on BigQuery.

    Returns:
        dict: A dictionary containing the health status. If successful, 
        returns {"status": "ok"}. If an error occurs, returns 
        {"status": "error", "details": <error_message>}.
    """
    try:
        client = bigquery.Client()
        client.query("SELECT 1").result()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.get("/filesdb")
async def list_files():
    """
    Fetches file metadata from a BigQuery table.

    Queries BigQuery for file details like name, URL, download time, type, 
    and status, ordered by download time (latest first).

    Returns:
        dict: List of file metadata as dictionaries.

    Raises:
        GoogleAPIError: On BigQuery API issues.
        ValueError: If required environment variables are missing.
    """

    client = bigquery.Client()
    query = f"""
        SELECT filename, url, downloaded_at, file_type, status
        FROM `{os.getenv("BIGQUERY_PROJECT")}.{os.getenv("BIGQUERY_DATASET")}.file_metadata`
        ORDER BY downloaded_at DESC
    """
    rows = client.query(query).result()
    return {"files": [dict(row) for row in rows]}