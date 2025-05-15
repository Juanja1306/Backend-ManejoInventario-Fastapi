# app/database.py

import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings

# 1. Construye el ODBC connection string exactamente como en tu script de prueba
odbc_str = (
    f"DRIVER={{{settings.DRIVER}}};"
    f"SERVER={settings.DB_SERVER},{settings.DB_PORT};"
    f"DATABASE={settings.DB_NAME};"
    f"UID={settings.DB_USER};"
    f"PWD={settings.DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)

# 2. URL-escapa toda la cadena
quoted = urllib.parse.quote_plus(odbc_str)

# 3. Monta la URL de SQLAlchemy usando odbc_connect
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quoted}"

# 4. Crea el engine y la sesión
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,         # detecta conexiones muertas
    pool_size=10,               # conexiones “en reposo” en el pool (minimas)
    max_overflow=20,            # conexiones extra bajo demanda (+20 escalables hasta maximo de 10+20 = 30)
    pool_recycle=3600,          # recicla conexiones tras 1 h
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,     # evita overhead de expirar objetos
)

# 5. Dependencia de FastAPI para inyectar la sesión

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

