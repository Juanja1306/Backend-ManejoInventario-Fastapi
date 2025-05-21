# routers/product_routes.py

from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import verificar_rol_tecnico
from app.schemas.producto import SolicitudProducto

router = APIRouter()


@router.post("/solicitudes")
async def crear_solicitud(solicitud: SolicitudProducto, usuario: dict = Depends(verificar_rol_tecnico)):
    # Aquí va la lógica para guardar la solicitud
    return {
        "message": "Solicitud creada",
        "usuario": usuario.correo,
        "producto_id": solicitud.producto_id,
        "cantidad": solicitud.cantidad
    }