from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

class ProductoPeticionSchema(BaseModel):
    idPeticionProducto: Optional[int] = None
    idPeticion: int
    idInventario: int
    producto: str
    cantidad: float
    estado: str
    comentario: str
    procesado: str
    numOrden: str
    entregadoA: str
    solicitadaEntregada: int
    cantidadProcesada: float
    fechaAtendida: date
    fechaCreacion: datetime
    fechaModificacion: datetime
    creadoPor: str
    modificadoPor: str

    model_config = ConfigDict(from_attributes=True)
