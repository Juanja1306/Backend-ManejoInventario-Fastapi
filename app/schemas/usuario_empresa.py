from typing import Optional
from pydantic import BaseModel, ConfigDict

class UsuarioEmpresaSchema(BaseModel):
    idAutoincrement: Optional[int] = None
    idUsuario: int
    ruc: str

    model_config = ConfigDict(from_attributes=True)