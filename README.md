# 📊 EMBRAPA Data Downloader API

A simple FastAPI application that downloads datasets from [EMBRAPA's Vitibrasil portal](http://vitibrasil.cnpuv.embrapa.br/download/) and stores them locally for further use in machine learning pipelines. Used as a tech challenge for the [FIAP Machine Learning Engineering](https://postech.fiap.com.br/curso/machine-learning-engineering/) program.

---

## 🚀 Features

- ✅ Download all `.csv` files from EMBRAPA
- 🧾 Log downloaded file metadata into a Postgres database
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
- Databases + asyncpg (PostgreSQL client)

---

## 🛠️ Setup 

### 1. Clone the repository

```bash
git clone https://github.com/seu-usuario/tech-challenge1-g27.git
cd tech-challenge1-g27
```

### 2. Create a `.env` file

Add a `.env` file in the project root with the following variable:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db_name>
```

You can get this from platforms like Render or other PostgreSQL providers.

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
Basic welcome route.

### `POST /download`
🔽 Triggers the download of all available `.csv` files from EMBRAPA's Vitibrasil portal.

- ✅ Saves the files locally in the `embrapa_files/` folder  
- 🧾 Logs metadata into a PostgreSQL database

### `GET /files`
📂 Lists all files currently saved in the `embrapa_files/` directory.

### `GET /files/{filename}`
📥 Downloads a specific file from local storage.

- 🔍 Returns `404` if the file is not found.

### `GET /filesdb`
🧾 Lists metadata of all downloaded files, as stored in the database.

- 📌 Sorted by download time (most recent first)

### `GET /health`
⚙️ Optional health check (if exposed) to verify if the database connection is operational.
---

## 🧪 Coming Soon

- [X] Endpoint to list available files  
- [X] Integration with Postgres database
- [ ] Integration with task scheduling or Celery for automatic updates

---

## 👨‍💻 Authors

- Victor Santos – [@vlsoexecutivo](mailto:vlsoexecutivo@gmail.com)
- G27 team – FIAP Tech Challenge 1

---

## 📄 License

MIT License
