# app/database2.py

import urllib
from functools import lru_cache

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SecondSettings(BaseSettings):
    """Configuración para la segunda base de datos (prefijo DB2_)."""
    DB2_USER: str
    DB2_PASSWORD: str
    DB2_SERVER: str
    DB2_PORT: int
    DB2_NAME: str
    DB2_DRIVER: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache()
def get_settings2() -> SecondSettings:
    """Carga y cachea la configuración desde variables de entorno."""
    return SecondSettings()

# Solo se lee settings una vez
settings2 = get_settings2()

# Construye el connection string ODBC y lo URL-escapa
odbc_str2 = (
    f"DRIVER={{{settings2.DB2_DRIVER}}};"
    f"SERVER={settings2.DB2_SERVER},{settings2.DB2_PORT};"
    f"DATABASE={settings2.DB2_NAME};"
    f"UID={settings2.DB2_USER};"
    f"PWD={settings2.DB2_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)
DATABASE_URL2 = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str2)}"

# Crea el engine una sola vez al importar el módulo
engine2 = create_engine(
    DATABASE_URL2,
    echo=True,
    pool_pre_ping=True,    # detecta conexiones muertas
    pool_size=5,           # tamaño mínimo del pool
    max_overflow=10,       # conexiones extra bajo demanda
    pool_recycle=3600,     # recicla conexiones tras 1 h
)

# sessionmaker global reutilizando el mismo engine
SessionLocal2 = sessionmaker(
    bind=engine2,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_db2():
    """
    Dependencia de FastAPI para inyectar la sesión de la segunda BD.
    Uso en endpoint: db: Session = Depends(get_db2)
    """
    db = SessionLocal2()
    try:
        yield db
    finally:
        db.close()
