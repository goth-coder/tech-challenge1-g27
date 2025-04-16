import os 
import aiohttp
from .constants import BASE_URL, DEST_FOLDER
from bs4 import BeautifulSoup 
from datetime import datetime
from db.database import database
from db.models import FileRecord
 

async def download_all_files():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(BASE_URL) as response:
                if response.status != 200:
                    return {"error": f"Site unavailable (status code {response.status})"}

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                links = soup.find_all("a")

                results = []

                for link in links:
                    href = link.get("href")
                    is_valid = href.endswith(".csv") and not href.startswith("?") and not href.startswith("#")
                    if href and is_valid:
                        file_url = BASE_URL + href
                        filename = os.path.basename(href)
                        file_path = os.path.join(DEST_FOLDER, filename)

                        try:
                            async with session.get(file_url) as file_response:
                                if file_response.status == 200:
                                    with open(file_path, "wb") as f:
                                        f.write(await file_response.read())

                                    # Salvar metadados no banco
                                    query = FileRecord.__table__.insert().values(
                                        filename=filename,
                                        url=file_url,
                                        downloaded_at=datetime.utcnow(),
                                        file_type=filename.split('.')[-1],
                                        status="success"
                                    )
                                    await database.execute(query)

                                    results.append({"file": filename, "status": "success"})

                                else:
                                    results.append({"file": filename, "status": f"error {file_response.status}"})

                        except Exception as e:
                            results.append({"file": filename, "status": f"error: {str(e)}"})

                return results

        except Exception as e:
            return {"error": f"Failed to fetch page: {str(e)}"}
 