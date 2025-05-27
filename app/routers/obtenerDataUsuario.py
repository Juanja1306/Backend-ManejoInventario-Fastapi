from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from app.utils import decode_jwt
from sqlalchemy.orm import Session                
from app.database import get_db                     
from app.models import Organizacion, UsuarioOrganizacion                 
from app.schemas.organizacion import OrganizacionRead  
from app.schemas.empresa import EmpresaRead
from app.schemas.rol import RolRead

router = APIRouter(
    prefix="/user",
    tags=["Obtener Empresa, Rol y Organizaciones"],
)

@router.get(
    "/empresa",
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
    "/rol",
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

@router.get(
    "/organizacion",
    summary="Obtener lista de organizaciones del usuario",
    response_model=List[OrganizacionRead])
def get_organizaciones(
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db)) -> List[OrganizacionRead]:
    """
    Extrae de la base de datos la lista de códigos de organizaciones del usuario.
    """
    # Extrae el correo del usuario del JWT
    correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)

    # Consulta la tabla de relación usuario-organización
    cod_orgs = {
        uo.codOrg
        for uo in db.query(UsuarioOrganizacion)
            .filter(UsuarioOrganizacion.correoUsuario == correo)
    }
    # Devuelve la lista de OrganizacionRead con cada código
    return [OrganizacionRead(nombre=c) for c in sorted(cod_orgs)]

