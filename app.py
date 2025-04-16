from fastapi import FastAPI
from scraper.download import download_all_files

app = FastAPI()

@app.get("/")
def root():
    return {"message": "EMBRAPA Data Downloader API"}

@app.post("/download")
def trigger_download():
    result = download_all_files()
    return {"status": result}
