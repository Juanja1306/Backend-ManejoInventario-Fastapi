from fastapi import APIRouter, Depends, Body, HTTPException
from app.utils import require_role
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Peticion
from app.models import ProductoPeticion as ProductoPeticionModel
from app.schemas.producto import ProductoPeticionRead
from app.schemas.peticion import PeticionRead

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



