from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PeticionSchema(BaseModel):
    idPeticion: Optional[int] = None
    solicitante: str
    categoria: str
    estado: str
    empresa: str
    rucEmpresa: str
    fecha: datetime
    fechaCreacion: datetime
    fechaModificacion: datetime
    creadoPor: str
    modificadoPor: str

    model_config = ConfigDict(from_attributes=True)
