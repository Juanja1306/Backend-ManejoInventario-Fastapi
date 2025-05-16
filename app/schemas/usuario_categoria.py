from typing import Optional
from pydantic import BaseModel, ConfigDict

class UsuarioCategoriaSchema(BaseModel):
    idAutoincrement: Optional[int] = None
    idUsuario: int
    idCategoria: str

    model_config = ConfigDict(from_attributes=True)
