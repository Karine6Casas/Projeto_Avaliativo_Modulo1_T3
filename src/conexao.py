# ========================================================
# Conexão com o PostgreSQL usando credenciais protegidas
# ========================================================

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

RAIZ = Path(__file__).resolve().parent.parent

# Lê o arquivo credenciais.env

load_dotenv(RAIZ / "credenciais.env")


def criar_engine():
    # Cria e devolve a conexão com o banco de dados
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )
    return create_engine(url)