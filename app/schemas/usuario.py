from typing import Optional
from pydantic import BaseModel, ConfigDict

class UsuarioSchema(BaseModel):
    idUsuario: Optional[int] = None      # PK opcional
    correoUsuario: str
    rolcategoria: str
    modificadoPor: str

    # Para que Pydantic pueda leer instancias ORM
    model_config = ConfigDict(from_attributes=True)
    
