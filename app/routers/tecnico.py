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
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/tecnico", tags=["Tecnico"], dependencies=[require_role(["tecnico"])])



@router.post(
    "/solicitud",
    summary="Crear solicitud de productos",
    status_code=201
)
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

    # Insertar nueva petición en la tabla tblPeticiones_bck
    # Calcular siguiente idPeticion manualmente
    last = db.query(Peticion.idPeticion).order_by(Peticion.idPeticion.desc()).first()
    next_id = (last[0] + 1) if last else 1
    now = datetime.now(ZoneInfo("America/Guayaquil"))
    try:
        # Crear y guardar la petición
        pet = Peticion(
            idPeticion=next_id,
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
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la petición: {str(e)}")

    # Procesar productos para guardar en tblProductosPeticion
    inv_map = {inv.idInventario: inv for inv in invs}
    # Calcular siguiente idPeticionProducto
    last_pp = db.query(ProductoPeticionModel.idPeticionProducto).order_by(ProductoPeticionModel.idPeticionProducto.desc()).first()
    next_pp = (last_pp[0] + 1) if last_pp else 1
    try:
        for p in productos:
            inv = inv_map[p.idInventario]
            pp = ProductoPeticionModel(
                idPeticionProducto=next_pp,
                idPeticion=next_id,
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
            next_pp += 1
        # Guardar todos los productos de petición
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la petición: {str(e)}")



