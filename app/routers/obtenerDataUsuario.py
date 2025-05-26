from typing import List, Dict, Any
from fastapi import APIRouter, Depends

from app.utils import decode_jwt

router = APIRouter(
    prefix="",
    tags=["Obtener Empresa y Rol"]
)

@router.get(
    "/get_empresa",
    summary="Obtener lista de RUCs de empresas del usuario",
    response_model=List[str])
def get_empresas(payload: Dict[str, Any] = Depends(decode_jwt)) -> List[str]:
    """
    Extrae del JWT la lista de RUCs de las empresas asociadas al usuario.
    """
    empresas: List[str] = []
    for um in payload.get("usuario_meta", []):
        for app in um.get("usuario-meta", []):
            for comp in app.get("app-meta", []):
                nombre = comp.get("empresa")
                if nombre and nombre not in empresas:
                    empresas.append(nombre)
    return empresas

@router.get(
    "/get_rol",
    summary="Obtener lista de roles del usuario",
    response_model=List[str])
def get_rol(payload: Dict[str, Any] = Depends(decode_jwt)) -> List[str]:
    """
    Extrae del JWT todos los roles únicos que tenga el usuario.
    """
    roles: List[str] = []
    for um in payload.get("usuario_meta", []):
        for app in um.get("usuario-meta", []):
            for comp in app.get("app-meta", []):
                for rol in comp.get("roles", []):
                    if rol and rol not in roles:
                        roles.append(rol)
    return roles
