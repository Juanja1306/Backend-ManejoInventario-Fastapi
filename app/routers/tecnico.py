#tecnico.py

from fastapi import APIRouter, Depends, Body, HTTPException
from app.utils import require_role, decode_jwt
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Inventario, Peticion
from app.models import ProductoPeticion as ProductoPeticionModel
from app.schemas.producto import ProductoPeticion
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/tecnico", tags=["Tecnico"], dependencies=[require_role(["TECNICO"])])


@router.post("/solicitud", summary="Crear solicitud de productos", status_code=201)
def create_solicitud(
    productos: List[ProductoPeticion] = Body(...),
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db)) -> None:
    # Extraer correo del usuario
    correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)
    # IDs recibidos
    ids = [p.idInventario for p in productos]
    # Consultar inventarios
    invs = db.query(Inventario).filter(Inventario.idInventario.in_(ids)).all()
    if len(invs) != len(ids):
        raise HTTPException(status_code=404, detail="Alguno de los productos no existe")
    # Verificar misma empresa
    rucs = {inv.rucEmpresa for inv in invs}
    if len(rucs) != 1:
        raise HTTPException(status_code=400, detail="Productos pertenecen a empresas distintas")
    rucEmpresa = rucs.pop()
    # Extraer categorías
    categorias = [inv.categoria for inv in invs]
    # Comprobar que la cantidad solicitada de cada producto no exceda el inventario antes de crear la petición
    inv_map_check = {inv.idInventario: inv for inv in invs}
    for p in productos:
        inv = inv_map_check[p.idInventario]
        if p.cantidad > inv.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Cantidad solicitada ({p.cantidad}) del producto {p.idInventario} excede inventario disponible ({inv.cantidad})"
            )

    # Hora local de Guayaquil (UTC-5 fijo)
    now = datetime.now(timezone(timedelta(hours=-5)))
    try:
        # Crear y añadir la petición principal (idPeticion generada por SQL Server)
        pet = Peticion(
            solicitante=correo,
            categoria=None,
            estado="Pendiente",
            empresa=invs[0].empresa,
            rucEmpresa=rucEmpresa,
            fecha=now,
            fechaCreacion=now,
            fechaModificacion=now,
            creadoPor=correo,
            modificadoPor=correo
        )
        db.add(pet)
        # Flush para obtener idPeticion asignado
        db.flush()
        # Procesar e insertar productos asociados usando pet.idPeticion
        inv_map = {inv.idInventario: inv for inv in invs}
        for p in productos:
            inv = inv_map[p.idInventario]
            pp = ProductoPeticionModel(
                idPeticion=pet.idPeticion,
                idInventario=p.idInventario,
                producto=inv.producto,
                cantidad=p.cantidad,
                estado="Pendiente",
                comentario=None,
                procesado=None,
                numOrden=None,
                entregadoA=None,
                solicitadaEntregada=None,
                cantidadProcesada=None,
                fechaCreacion=now,
                fechaModificacion=now,
                creadoPor=correo,
                modificadoPor=correo
            )
            db.add(pp)
        # Confirmar toda la transacción
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la solicitud: {str(e)}")



