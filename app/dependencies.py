# dependencies.py
from fastapi import Depends, HTTPException
from app.schemas.auth import TokenData
from app.utils import verificar_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> TokenData:
    return verificar_token(token)

async def verificar_rol_tecnico(usuario: TokenData = Depends(obtener_usuario_actual)):
    if "bodega" not in usuario.roles.values():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Rol insuficiente"
        )
    return usuario