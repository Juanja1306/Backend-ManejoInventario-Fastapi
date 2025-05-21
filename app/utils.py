# utils.py
from datetime import datetime, timedelta
import jwt
from typing import Dict
from app.schemas.auth import TokenData
from dotenv import load_dotenv
import os

from fastapi import HTTPException, status
from jwt import PyJWTError


load_dotenv()

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")
PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH")

# Carga tu clave privada en formato PEM
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")


def crear_token_acceso(data: TokenData) -> str:
    payload = data.dict()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

def verificar_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )