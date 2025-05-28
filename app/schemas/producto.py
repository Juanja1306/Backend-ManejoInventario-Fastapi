# schemas/producto.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

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

class ProductoPeticion(BaseModel):
    idInventario: int
    cantidad: float

    class Config:
        json_schema_extra = {
            "example": {
                "idInventario": 1,
                "cantidad": 1
            }
        }

class ProductoPeticionRead(BaseModel):
    idPeticionProducto: int
    idPeticion: Optional[int]
    idInventario: Optional[int]
    producto: Optional[str]
    cantidad: Optional[float]
    estado: Optional[str]
    comentario: Optional[str]
    procesado: Optional[str]
    numOrden: Optional[str]
    entregadoA: Optional[str]
    solicitadaEntregada: Optional[int]
    cantidadProcesada: Optional[float]
    fechaAtendida: Optional[date]
    fechaCreacion: Optional[datetime]
    fechaModificacion: Optional[datetime]
    creadoPor: Optional[str]
    modificadoPor: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "idPeticionProducto": 1023,
                "idPeticion": 619,
                "idInventario": 16125,
                "producto": "UMEJE007",
                "cantidad": 1,
                "estado": "Entregado",
                "comentario": "OK",
                "procesado": "Si",
                "numOrden": "0623176",
                "entregadoA": "MANUEL MAZA",
                "solicitadaEntregada": 0,
                "cantidadProcesada": 1.0,
                "fechaAtendida": "2025-05-13",
                "fechaCreacion": "2025-05-13 16:37:44.553",
                "fechaModificacion": "2025-05-13 16:39:21.733",
                "creadoPor": "FAUSTO NESTORIO MENDEZ ATANCURI",
                "modificadoPor": "JAIME SEBASTIAN URDIALES LANDY"
            }
        }

