import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/download/"
DEST_FOLDER = "embrapa_files"

def download_all_files():
    os.makedirs(DEST_FOLDER, exist_ok=True)

    try:
        response = requests.get(BASE_URL, timeout=10)

        # Verifies if HTTP response is 200 (OK)
        if response.status_code != 200:
            print(f"⚠️ Site responded with status {response.status_code}")
            return f"Failed to access site: status code {response.status_code}"

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return "Failed to connect. Site may be offline or unreachable."
    
    # Continues if the connection is successful
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a", href=True):
        file_url = urljoin(BASE_URL, link["href"])
        if file_url.endswith(".csv"):
            file_name = file_url.split("/")[-1]
            file_path = os.path.join(DEST_FOLDER, file_name)
            
            try:
                print(f"⬇️  Downloading {file_name}...")
                file_response = requests.get(file_url)
                with open(file_path, "wb") as f:
                    f.write(file_response.content)
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to download {file_name}: {e}")
                continue
    
    return f"✅ Download completed. Files saved to '{DEST_FOLDER}/'"

if __name__ == "__main__":
    download_all_files()
