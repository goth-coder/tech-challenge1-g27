import os
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine
from .models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Conexão assíncrona
database = Database(DATABASE_URL)

# Engine para criar tabelas
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))
Base.metadata.create_all(bind=engine)
