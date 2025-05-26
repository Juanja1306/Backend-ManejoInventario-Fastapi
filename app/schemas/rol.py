# app/schemas/rol.py
from pydantic import BaseModel

class RolRead(BaseModel):
    nombre: str

    class Config:
        schema_extra = {
            "example": {"nombre": "BODEGA"}
        }
