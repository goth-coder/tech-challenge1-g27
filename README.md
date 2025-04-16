# 📊 EMBRAPA Data Downloader API

A simple FastAPI application that downloads datasets from [EMBRAPA's Vitibrasil portal](http://vitibrasil.cnpuv.embrapa.br/download/) and stores them locally for further use in machine learning pipelines. Used as a tech challenge for the [FIAP Machine Learning Engineering](https://postech.fiap.com.br/curso/machine-learning-engineering/) program.

---

## 🚀 Features

- ✅ Download all `.csv` files from EMBRAPA
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

---

## 🛠️ Setup 

### 1. Clone the repository

```bash
git clone https://github.com/seu-usuario/tech-challenge1-g27.git
cd tech-challenge1-g27
```

### 2. Install dependencies with Poetry

```bash
poetry install
```

### 3. Activate the virtual environment

```bash
poetry shell
```

### 4. Run the API

```bash
uvicorn app:app --reload
```

---

## 📡 Endpoints

### `GET /`
Basic welcome route.

### `POST /download`
Triggers the download of files from EMBRAPA.

---

## 🧪 Coming Soon

- [ ] Endpoint to list available files  
- [ ] Integration with database

---

## 👨‍💻 Authors

- Victor Santos – [@vlsoexecutivo](mailto:vlsoexecutivo@gmail.com)
- G27 team – FIAP Tech Challenge 1

---

## 📄 License

MIT License
