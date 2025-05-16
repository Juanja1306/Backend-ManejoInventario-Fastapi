from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class InventarioSchema(BaseModel):
    idInventario: Optional[int] = None
    empresa: str
    rucEmpresa: str
    categoria: str
    producto: str
    descripcion: str
    cantidad: float
    costoUnitario: float
    costoTotal: float
    unidadMedida: str
    numOrden: str
    solicitadoPor: str
    ubicacion: str
    fechaCreacion: datetime
    fechaModificacion: datetime
    creadoPor: str
    modificadoPor: str

    model_config = ConfigDict(from_attributes=True)

