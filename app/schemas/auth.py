# schemas/auth.py
from pydantic import BaseModel
from typing import Dict, List

class TokenData(BaseModel):
    idUsuario: int
    correo: str
    roles: Dict[str, str]  # {aplicacion: rol}

class Credentials(BaseModel):
    correo: str
    contrasenia: str