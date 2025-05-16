from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RepuestoSchema(BaseModel):
    codRepuesto: str
    codJDE: str
    codFusion: str
    descripcion: str
    unidadMedida: str
    costoUnitario: float
    fechaCreacion: datetime
    fechaModificacion: datetime
    creadoPor: str
    modificadoPor: str

    model_config = ConfigDict(from_attributes=True)
