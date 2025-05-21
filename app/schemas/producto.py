# schemas/product.py
from pydantic import BaseModel

class SolicitudProducto(BaseModel):
    producto_id: int
    cantidad: int
