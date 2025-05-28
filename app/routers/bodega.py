from fastapi import APIRouter, Depends, Body, HTTPException
from app.utils import require_role, decode_jwt
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.database2 import get_db2
from app.models import Peticion
from app.models import ProductoPeticion as ProductoPeticionModel
from app.schemas.producto import ProductoPeticionRead, ProductoPeticionProcesando, ProductoPeticionProcesado, ProductoPeticionEntregado
from app.schemas.peticion import PeticionRead
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from sqlalchemy import text

router = APIRouter(prefix="/bodega", tags=["Bodega"], dependencies=[require_role(["BODEGA"])])

@router.get(
    "/pendientes",
    summary="Obtener productosPeticion de peticiones pendientes",
    response_model=List[ProductoPeticionRead]
)
def get_peticiones_pendientes(db: Session = Depends(get_db)) -> List[ProductoPeticionRead]:
    """
    Devuelve los registros de tblProductosPeticion donde estado='Pendiente' y comentario,
    procesado y fechaAtendida son NULL.
    """
    try:
        peticiones = db.query(ProductoPeticionModel).filter(
            ProductoPeticionModel.estado == "Pendiente",
            ProductoPeticionModel.comentario == None,
            ProductoPeticionModel.procesado == None,
            ProductoPeticionModel.fechaAtendida == None
        ).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return peticiones


@router.get(
    "/pendientes/peticiones",
    summary="Obtener peticiones únicas con productos pendientes",
    response_model=List[PeticionRead]
)
def get_peticiones_pendientes_unicas(db: Session = Depends(get_db)) -> List[PeticionRead]:
    """
    Devuelve las peticiones (tabla tblPeticiones) correspondientes a los productos
    en tblProductosPeticion con estado='Pendiente' y comentario, procesado y fechaAtendida NULL.
    Los IDs de petición se muestran una sola vez.
    """
    try:
        # Obtener IDs de petición únicos
        rows = (
            db.query(ProductoPeticionModel.idPeticion)
            .filter(
                ProductoPeticionModel.estado == "Pendiente",
                ProductoPeticionModel.comentario == None,
                ProductoPeticionModel.procesado == None,
                ProductoPeticionModel.fechaAtendida == None
            )
            .distinct()
            .all()
        )
        ids = [r[0] for r in rows]
        # Consultar peticiones únicas
        peticiones = (
            db.query(Peticion)
            .filter(Peticion.idPeticion.in_(ids))
            .all()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return peticiones


@router.post(
    "/pendientes/procesando",
    summary="Actualizar estado y comentario de producto de petición",
    status_code=200
)
def editar_producto_peticion(
    data: ProductoPeticionProcesando = Body(...),
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db)) -> None:
    """
    Actualiza un producto de petición: pone estado a 'Procesando', ajusta fechaAtendida a hora local UTC-5,
    y asigna comentario si se proporciona.
    """
    try:
        pp = db.query(ProductoPeticionModel).filter(
            ProductoPeticionModel.idPeticionProducto == data.idPeticionProducto
        ).first()
        if not pp:
            raise HTTPException(status_code=404, detail="ProductoPeticion no encontrado")
        # Solo procesar productos en estado 'Pendiente'
        if pp.estado != "Pendiente":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede procesar un producto en estado Pendiente (estado actual: {pp.estado})"
            )
        # Actualizar campos
        pp.estado = "Procesando"
        # Hora local de Guayaquil (UTC-5 fijo)
        now = datetime.now(timezone(timedelta(hours=-5)))
        pp.fechaAtendida = now.date()
        if data.comentario and data.comentario.strip():
            pp.comentario = data.comentario
        # Registrar quién y cuándo modificó
        correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)
        pp.modificadoPor = correo
        pp.fechaModificacion = now
        # Actualizar estado de la petición si hay al menos un producto en 'Procesando'
        children = db.query(ProductoPeticionModel).filter(
            ProductoPeticionModel.idPeticion == pp.idPeticion
        ).all()
        if any(item.estado == "Procesando" for item in children):
            pet_row = db.query(Peticion).filter(
                Peticion.idPeticion == pp.idPeticion
            ).first()
            if pet_row:
                pet_row.estado = "Procesando"
                pet_row.modificadoPor = correo
                pet_row.fechaModificacion = now
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/pendientes/listoParaEntregar",
    summary="Marcar productoPeticion como listo para entregar",
    status_code=200
)
def procesar_producto_peticion(
    data: ProductoPeticionProcesado = Body(...),
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db)) -> None:
    """
    Actualiza un producto de petición a 'Listo para Entregar', con comentario opcional,
    solicitadaEntregada (o 0), cantidadProcesada validada y registra quién y cuándo modificó.
    """
    pp = db.query(ProductoPeticionModel).filter(
        ProductoPeticionModel.idPeticionProducto == data.idPeticionProducto
    ).first()
    if not pp:
        raise HTTPException(status_code=404, detail="ProductoPeticion no encontrado")
    # Solo marcar 'Listo para Entregar' cuando esté en 'Procesando'
    if pp.estado != "Procesando":
        raise HTTPException(
            status_code=400,
            detail=f"Solo se puede marcar Listo para Entregar cuando el producto está en estado Procesando (actual: {pp.estado})"
        )
    # Validar cantidadProcesada
    if data.cantidadProcesada is not None and data.cantidadProcesada > pp.cantidad:
        raise HTTPException(status_code=400, detail="cantidadProcesada excede la cantidad requerida")
    # Actualizar campos
    pp.estado = "Listo para Entregar"
    pp.solicitadaEntregada = data.solicitadaEntregada if data.solicitadaEntregada is not None else 0
    if data.comentario and data.comentario.strip():
        pp.comentario = data.comentario
    if data.cantidadProcesada is not None:
        pp.cantidadProcesada = data.cantidadProcesada
    # Modificado por y fecha
    correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)
    pp.modificadoPor = correo
    now = datetime.now(timezone(timedelta(hours=-5)))
    pp.fechaModificacion = now
    # Actualizar estado de la petición si todos sus productos están Listo para Entregar
    iguales = db.query(ProductoPeticionModel).filter(
        ProductoPeticionModel.idPeticion == pp.idPeticion
    ).all()
    if iguales and all(item.estado == "Listo para Entregar" for item in iguales):
        pet_row = db.query(Peticion).filter(
            Peticion.idPeticion == pp.idPeticion
        ).first()
        if pet_row:
            pet_row.estado = "Listo para Entregar"
            # Actualizar quién y cuándo modificó la petición
            pet_row.modificadoPor = correo
            pet_row.fechaModificacion = now
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/pendientes/entregado",
    summary="Marcar productoPeticion como Entregado",
    status_code=200
)
def entregar_producto_peticion(
    data: ProductoPeticionEntregado = Body(...),
    payload: dict = Depends(decode_jwt),
    db: Session = Depends(get_db),
    db2: Session = Depends(get_db2)) -> None:
    """
    Actualiza un producto de petición a 'Entregado'. Verifica estado previo, aplica comentario opcional,
    asigna entregadoA, y sincroniza la petición madre.
    """
    try:
        # Validar que el correo entregadoA existe en la tabla tblUsuario de OtraDB
        row = db2.execute(
            text("SELECT 1 FROM tblUsuario WHERE correo = :correo"),
            {"correo": data.entregadoA}
            ).first()
        if not row:
            raise HTTPException(400, detail="Usuario no existe. Comunicarse con administrador para agregarlo en autentificacion-gig")
        pp = db.query(ProductoPeticionModel).filter(
            ProductoPeticionModel.idPeticionProducto == data.idPeticionProducto
        ).first()
        if not pp:
            raise HTTPException(status_code=404, detail="ProductoPeticion no encontrado")
        # Solo permitir marcar como Entregado si está en 'Listo para Entregar'
        if pp.estado != "Listo para Entregar":
            raise HTTPException(
                status_code=400,
                detail=f"Solo se puede marcar Entregado cuando el producto está en estado 'Listo para Entregar' (actual: {pp.estado})"
            )
        # Actualizar campos
        pp.estado = "Entregado"
        if data.comentario and data.comentario.strip():
            pp.comentario = data.comentario
        pp.entregadoA = data.entregadoA
        # Registrar quién y cuándo modificó
        correo = next((um.get("usuarioCorreo") for um in payload.get("usuario_meta", [])), None)
        now = datetime.now(timezone(timedelta(hours=-5)))
        pp.modificadoPor = correo
        pp.fechaModificacion = now
        # Sincronizar estado de la petición madre si todos los productos están entregados
        children = db.query(ProductoPeticionModel).filter(
            ProductoPeticionModel.idPeticion == pp.idPeticion
        ).all()
        if children and all(item.estado == "Entregado" for item in children):
            pet_row = db.query(Peticion).filter(
                Peticion.idPeticion == pp.idPeticion
            ).first()
            if pet_row:
                pet_row.estado = "Entregado"
                pet_row.modificadoPor = correo
                pet_row.fechaModificacion = now
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



