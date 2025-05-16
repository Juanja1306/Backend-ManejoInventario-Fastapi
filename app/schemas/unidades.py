from typing import Optional
from pydantic import BaseModel, ConfigDict

class UnidadSchema(BaseModel):
    idUnidad: Optional[int] = None
    unidad: str
    descripcion: str
    clase: str

    model_config = ConfigDict(from_attributes=True)
