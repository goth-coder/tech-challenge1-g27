import os 
from fastapi import FastAPI
from scraper.download import download_all_files
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "EMBRAPA Data Downloader API"}

@app.post("/download")
def trigger_download():
    result = download_all_files()
    return {"status": result}

@app.get("/files")
def list_files():
    try:
        files = os.listdir("embrapa_files")
        return {"files": files}
    except FileNotFoundError:
        return {"files": []}
    
@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = os.path.join("embrapa_files", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(file_path)