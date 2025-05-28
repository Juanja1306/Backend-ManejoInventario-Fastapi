# app/routers/asignarBodegas.py

from typing import List, Dict, Any
from fastapi import APIRouter, Body, Depends, HTTPException
from app.utils import require_role, decode_jwt
from sqlalchemy.orm import Session                
from app.database import get_db                     
from app.database2 import get_db2                  
from app.models import Organizacion, UsuarioOrganizacion                 
from app.schemas.organizacion import CodigoOrganizacion, UsuarioOrganizacionCreate
from sqlalchemy import text                         

router = APIRouter(
    prefix="/organizacion",
    tags=["Asignar Bodegas"], 
    dependencies=[require_role(["BODEGA"])]
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
    status_code=201
)
def post_organizacion(
    data: UsuarioOrganizacionCreate = Body(...),
    db: Session = Depends(get_db),
    db2: Session = Depends(get_db2)) -> None:
    """
    Agrega una organización al usuario usando el correo y código recibidos en el JSON.
    """
    correo = data.correo
    cod_org = data.codigo
    # Validar que el usuario existe en la tabla tblUsuario de la otra BD
    exists = db2.execute(
        text("SELECT 1 FROM tblUsuario WHERE correo = :correo"),
        {"correo": correo}
    ).first()
    if not exists:
        raise HTTPException(400, detail="Usuario no existe. Comunicarse con administrador para agregarlo en autentificacion-gig")
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
    # Devuelve 201 OK sin contenido


