# 📊 EMBRAPA Data Downloader API

A simple FastAPI application that downloads datasets from [EMBRAPA's Vitibrasil portal](http://vitibrasil.cnpuv.embrapa.br/download/) and stores them locally for further use in machine learning pipelines. Developed as part of the [FIAP Machine Learning Engineering](https://postech.fiap.com.br/curso/machine-learning-engineering/) program.

---

## 🚀 Features

- ✅ Download all `.csv` files from EMBRAPA  
- 🧾 Log downloaded file metadata into a **BigQuery** table  
- 🌐 Simple HTTP API built with FastAPI  
- 🛡️ Handles connection errors (e.g., offline site)  
- 📂 Saves files in a dedicated local directory (`embrapa_files/`)

---

## 🧰 Tech Stack

- Python 3.11+  
- FastAPI  
- Requests  
- BeautifulSoup4  
- Uvicorn (for dev server)  
- Poetry (for dependency management)  
- Google Cloud BigQuery (`google-cloud-bigquery`)  
- `python-dotenv` for environment management  

---

## 🛠️ Setup 

### 1. Clone the repository

```bash
git clone https://github.com/seu-usuario/tech-challenge1-g27.git
cd tech-challenge1-g27
```

### 2. Create a `.env` file

In the project root, add a `.env` file with the following variables:

```env
GOOGLE_APPLICATION_CREDENTIALS=secrets/your-key.json
BIGQUERY_PROJECT=your-gcp-project-id
BIGQUERY_DATASET=your_dataset_name
```

Replace `your-key.json` with the path to your service account JSON, and the project/dataset values accordingly.

### 3. Install dependencies with Poetry

```bash
poetry install
```

### 4. Activate the virtual environment

```bash
poetry shell
```

### 5. Run the API

```bash
uvicorn app:app --reload
```

---

## 📡 Endpoints

### `GET /`  
Returns a welcome message.

### `POST /download`  
🔽 Triggers the download of all `.csv` files from EMBRAPA's Vitibrasil portal.  
- ✅ Saves files to `embrapa_files/`  
- 🧾 Logs metadata to **BigQuery**

### `GET /files`  
📂 Lists all downloaded files in the `embrapa_files/` directory.

### `GET /preview/{filename}`  
📥 Downloads a specific file.  
- 🔍 Returns `404` if not found.

### `GET /filesdb`  
🧾 Lists all logged file metadata from BigQuery.  
- 📌 Sorted by download time (newest first)

### `GET /health`  
⚙️ Verifies if the BigQuery connection is working.

---

## 🧪 Coming Soon

- [X] Async download of all Vitibrasil files  
- [X] Metadata logging to BigQuery  
- [X] File preview in Swagger docs  
- [ ] Replace `poetry` with [`uv`](https://github.com/astral-sh/uv)  
- [ ] Replace Render with Supabase  
- [ ] Replace `aiohttp` with `httpx`  
- [ ] Define structured Pydantic models  
- [ ] DataFrame integration  
- [ ] Store dataset contents (not just metadata) in BigQuery  
- [ ] Schedule automatic updates (Celery or GCP Scheduler)  
- [ ] Data cleaning and preprocessing utilities

---

## 👨‍💻 Authors

- Victor Santos – [@vlsoexecutivo](mailto:vlsoexecutivo@gmail.com)  
- G27 Team – FIAP Tech Challenge 1

---

## 📄 License

MIT License 