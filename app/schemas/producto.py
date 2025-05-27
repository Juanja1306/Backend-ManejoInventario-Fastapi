# schemas/producto.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InventarioRead(BaseModel):
    idInventario: int
    empresa: Optional[str]
    rucEmpresa: Optional[str]
    categoria: Optional[str]
    producto: Optional[str]
    descripcion: Optional[str]
    cantidad: Optional[float]
    unidadMedida: Optional[str]
    ubicacion: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "idInventario": 1,
                "empresa": "Graiman",
                "rucEmpresa": "0190122271001",
                "categoria": "REPUESTOS ACTIVADOS",
                "producto": "RP034304",
                "descripcion": "JUEGO CADENA COMPLETA P/20 CANASTILLAS SECAD EVR11",
                "cantidad": 1,
                "unidadMedida": "UN",
                "ubicacion": "01.01.00.00"
            }
        }

class ProductoId(BaseModel):
    idInventario: int

    class Config:
        json_schema_extra = {
            "example": {
                "idInventario": 1
            }
        }


class ProductoResumen(BaseModel):
    rucEmpresa: str
    categorias: List[str]