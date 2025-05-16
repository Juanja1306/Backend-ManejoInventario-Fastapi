from typing import Optional
from pydantic import BaseModel, ConfigDict

class RolSchema(BaseModel):
    idRoles: Optional[int] = None
    descripcion: str

    model_config = ConfigDict(from_attributes=True)
