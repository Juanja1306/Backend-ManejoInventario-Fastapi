# utils.py
from datetime import datetime, timedelta
import jwt
from typing import Dict, Any, List
from dotenv import load_dotenv
import os

from fastapi import HTTPException, status, Depends
from jwt import PyJWTError

from fastapi.security import OAuth2PasswordBearer


load_dotenv()

PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH")

# Carga tu clave privada en formato PEM

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = os.getenv("ALGORITHM")

        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_jwt(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Valida firma/expiración y devuelve el payload completo del JWT.
    Esta dependencia se encarga de rechazar un token inválido o expirado.
    """
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_roles: List[str]):
    """
    Crea una dependencia que comprueba que en el payload exista
    al menos uno de los roles pedidos en cualquier app-meta.
    """
    def checker(payload: Dict[str, Any] = Depends(decode_jwt)):
        usuario_meta = payload.get("usuario_meta", [])
        # “usuario_meta” -> lista de usuarios (normalmente 1) ->
        # cada uno tiene "usuario-meta" → lista de apps → cada una:
        # { "app-meta": [ { "roles": [...] }, … ] }
        for um in usuario_meta:
            for app_entry in um.get("usuario-meta", []):
                for comp in app_entry.get("app-meta", []):
                    roles = comp.get("roles", [])
                    if any(r in roles for r in required_roles):
                        return payload
                    
        # si llego aquí, no encontró ninguno de los roles requeridos
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Se requiere uno de estos roles: {required_roles}"
        )
    return Depends(checker)
