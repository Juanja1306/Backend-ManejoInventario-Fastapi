from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PeticionRead(BaseModel):
    idPeticion: int
    solicitante: Optional[str]
    estado: Optional[str]
    empresa: Optional[str]
    rucEmpresa: Optional[str]
    fechaCreacion: Optional[datetime]
    fechaModificacion: Optional[datetime]
    creadoPor: Optional[str]
    modificadoPor: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "idPeticion": 618,
                "solicitante": "JOHN ALEXANDER FAREZ BENALCAZAR",
                "estado": "Pendiente",
                "empresa": "Empresa X",
                "rucEmpresa": "1234567890",
                "fechaCreacion": "2021-01-01",
                "fechaModificacion": "2021-01-01",
                "creadoPor": "Usuario",
                "modificadoPor": "Usuario"
            }
        }
    
