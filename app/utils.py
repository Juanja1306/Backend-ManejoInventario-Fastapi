# utils.py optimized
import os
from functools import lru_cache
from typing import Any, Dict, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from pydantic_settings import BaseSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Settings(BaseSettings):
    """
    Configuración de entorno para JWT.
    """
    public_key_path: str
    algorithm: str

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

@lru_cache()
def get_public_key() -> bytes:
    """
    Lee y cachea la clave pública desde el fichero PEM.
    """
    settings = get_settings()
    path = settings.public_key_path
    if not os.path.isfile(path):
        raise RuntimeError(f"Public key file not found: {path}")
    with open(path, "rb") as f:
        return f.read()


def decode_jwt(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependencia para validar y decodificar el JWT.
    Lanza 401 si el token es inválido o expirado.
    """
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            get_public_key(),
            algorithms=[settings.algorithm]
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_roles: List[str]):
    """
    Crea una dependencia que verifica que el usuario tenga al menos
    uno de los roles indicados.

    Uso:
        @router.get(..., dependencies=[require_role(["ADMIN"])])
    """
    def checker(payload: Dict[str, Any] = Depends(decode_jwt)) -> Dict[str, Any]:
        usuario_meta = payload.get("usuario_meta", [])
        has_role = any(
            role in comp.get("roles", [])
            for um in usuario_meta
            for app in um.get("usuario-meta", [])
            for comp in app.get("app-meta", [])
            for role in required_roles
        )
        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de estos roles: {required_roles}",
            )
        return payload

    return Depends(checker)

def require_app(required_app: str):
    """
    Crea una dependencia que valida que el usuario tenga acceso a la app indicada.
    """
    def checker(payload: Dict[str, Any] = Depends(decode_jwt)) -> Dict[str, Any]:
        apps = [
            app_entry.get("nombre-app")
            for um in payload.get("usuario_meta", [])
            for app_entry in um.get("usuario-meta", [])
        ]
        if required_app not in apps:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere acceso a la aplicación '{required_app}'"
            )
        return payload

    return Depends(checker)
