# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import httpx
from typing import Dict
from app.schemas.auth import Credentials, TokenData
from app.utils import crear_token_acceso, verificar_token

from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
AUTH_BACKEND_URL = os.getenv("AUTH_BACKEND_URL")

@router.post("/login")
async def login(credentials: Credentials):
    async with httpx.AsyncClient() as client:
        # Validar credenciales en backend de autenticación
        response = await client.post(
            AUTH_BACKEND_URL,
            json={"correo": credentials.correo, "contrasenia": credentials.contrasenia}
        )
    
    if response.status_code != 200:
        print("Error en la autenticación:", response.text)
        print("Credenciales:", response.status_code)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token JWT local
    user_data = response.json()
    token_data = TokenData(
        idUsuario=user_data["idUsuario"],
        correo=user_data["correo"],
        roles=user_data["roles"]
    )
    
    access_token = crear_token_acceso(token_data)
    return {"access_token": access_token, "token_type": "bearer"}
