from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from app.utils import decode_jwt

from app.schemas.empresa import EmpresaRead
from app.schemas.rol import RolRead

router = APIRouter(
    prefix="",
    tags=["Obtener Empresa y Rol"]
)

@router.get(
    "/get_empresa",
    summary="Obtener lista de RUCs de empresas del usuario",
    response_model=List[EmpresaRead])
def get_empresas(payload: dict = Depends(decode_jwt)) -> List[EmpresaRead]:
    """
    Extrae del JWT la lista de nombres de empresas asociadas al usuario.
    """
    nombres = {
        comp["empresa"]
        for um in payload.get("usuario_meta", [])
        for app in um.get("usuario-meta", [])
        for comp in app.get("app-meta", [])
        if comp.get("empresa")
    }
    # Convertimos cada string en el schema
    return [EmpresaRead(nombre=n) for n in sorted(nombres)]

@router.get(
    "/get_rol",
    summary="Obtener lista de roles del usuario",
    response_model=List[RolRead])
def get_rol(payload: dict = Depends(decode_jwt)) -> List[RolRead]:
    """
    Extrae del JWT todos los roles únicos que tenga el usuario.
    """
    nombres = {
        rol
        for um in payload.get("usuario_meta", [])
        for app in um.get("usuario-meta", [])
        for comp in app.get("app-meta", [])
        for rol in comp.get("roles", [])
        if rol
    }
    return [RolRead(nombre=r) for r in sorted(nombres)]

