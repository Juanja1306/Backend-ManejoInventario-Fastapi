# routers/producto.py

from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Inventario
from app.schemas.producto import InventarioRead

router = APIRouter(prefix="/producto", tags=["Producto"])

@router.get(
    "/",
    summary="Obtener productos filtrados por bodega, empresa y categoría",
    response_model=List[InventarioRead]
)
def get_productos(
    empresa: str = Query("all", description="Empresa o 'all' para todas"),
    ubicacion: str = Query("all", description="Ubicación o 'all' para todas"),
    categoria: str = Query("all", description="Categoría o 'all' para todas"),
    producto: str = Query("all", description="Código o 'all' para todas"),
    db: Session = Depends(get_db)
) -> List[InventarioRead]:
    """
    Devuelve los registros de inventario filtrados por bodega (ubicacion), empresa y categoria.
    Si alguno de los parámetros es 'all', no se filtra por ese campo.
    """
    query = db.query(Inventario)
    if ubicacion.lower() != "all":
        query = query.filter(Inventario.ubicacion == ubicacion)
    if empresa.lower() != "all":
        query = query.filter(Inventario.empresa == empresa)
    if categoria.lower() != "all":
        query = query.filter(Inventario.categoria == categoria)
    if producto.lower() != "all":
        query = query.filter(Inventario.producto == producto)
    return query.all()


