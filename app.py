import os 
from fastapi import FastAPI
from scraper.download import download_all_files
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from db.database import database
from db.models import FileRecord

app = FastAPI()


@app.get("/")
def root():
    return {"message": "EMBRAPA Data Downloader API"}

@app.post("/download")
async def trigger_download():
    result = await download_all_files()
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


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/health")
async def health_check():
    try:
        await database.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@app.get("/filesdb")
async def list_files():
    query = FileRecord.__table__.select().order_by(FileRecord.downloaded_at.desc())
    results = await database.fetch_all(query)
    return {"files": results}    