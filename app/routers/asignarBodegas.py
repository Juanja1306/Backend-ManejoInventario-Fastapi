# app/routers/asignarBodegas.py

from typing import List, Dict, Any
from fastapi import APIRouter, Body, Depends, HTTPException
from app.utils import decode_jwt
from sqlalchemy.orm import Session                
from app.database import get_db                     
from app.models import Organizacion, UsuarioOrganizacion                 
from app.schemas.organizacion import OrganizacionRead  
from app.schemas.organizacion import CodigoOrganizacion

router = APIRouter(
    prefix="/organizacion",
    tags=["Asignar Bodegas"]
)


@router.get(
    "/codigos",
    summary="Obtener lista de códigos de todas las organizaciones de la base de datos",
    response_model=List[CodigoOrganizacion]
)
def get_codigos_organizaciones(db: Session = Depends(get_db)) -> List[CodigoOrganizacion]:
    """
    Devuelve de la tabla tblOrganizaciones solamente los códigos de organización.
    """
    codigos = { org.codigo for org in db.query(Organizacion).all() }
    return [CodigoOrganizacion(nombre=cod) for cod in sorted(codigos)]


@router.post(
    "/agregar",
    summary="Agregar una organización al usuario",
    response_model=OrganizacionRead
)
def post_organizacion(
    data: CodigoOrganizacion,
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db)) -> OrganizacionRead:
    """
    Agrega una organización al usuario usando el correo del JWT
    y el código de organización recibido en el JSON.
    """
    # Extrae el correo del usuario del JWT
    correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)
    # Extrae el código de la organización del body
    cod_org = data.nombre
    # Busca la organización en la base de datos
    org = db.query(Organizacion).filter(Organizacion.codigo == cod_org).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organización no encontrada")
    
    # Revisa si la relación ya existe
    if db.query(UsuarioOrganizacion).filter(UsuarioOrganizacion.correoUsuario == correo, UsuarioOrganizacion.codOrg == cod_org).first():
        raise HTTPException(status_code=400, detail="La organización ya está asignada al usuario")
    
    # Guarda la relación en tblUsuarioOrganizacion
    db.add(UsuarioOrganizacion(correoUsuario=correo, codOrg=cod_org))
    db.commit()
    # Devuelve el código asignado para confirmación
    return OrganizacionRead(nombre=cod_org)

