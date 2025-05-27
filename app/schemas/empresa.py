# app/schemas/empresa.py
from pydantic import BaseModel

class EmpresaRead(BaseModel):
    nombre: str

    class Config:
        json_schema_extra  = {
            "example": {"nombre": "VANDERBILT"}
        }
