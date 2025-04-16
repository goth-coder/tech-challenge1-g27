import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"
DEST_FOLDER = "embrapa_files"

def download_all_files():
    os.makedirs(DEST_FOLDER, exist_ok=True)

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        file_url = urljoin(BASE_URL, link["href"])
        if file_url.endswith(".csv"):
            file_name = file_url.split("/")[-1]
            file_path = os.path.join(DEST_FOLDER, file_name)

            print(f"⬇️  Downloading {file_name}...")
            file_response = requests.get(file_url)
            with open(file_path, "wb") as f:
                f.write(file_response.content)
    
    return f"✅ Download completed. Files saved to '{DEST_FOLDER}/'"

if __name__ == "__main__":
    download_all_files()
