from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AuditoriaSchema(BaseModel):
    idAuditoria: Optional[int] = None
    empresa: str
    rucEmpresa: str
    categoria: str
    producto: str

    descripcion:   Optional[str]     = None
    unidadMedida:  Optional[str]     = None
    costoTotal:    Optional[float]   = None
    cantidad:      Optional[float]   = None
    motivo:        Optional[str]     = None
    comentarios:   Optional[str]     = None
    saldoInicial:  Optional[float]   = None
    saldoFinal:    Optional[float]   = None

    fechaSolicitada: Optional[datetime] = None
    fechaProcesada:  Optional[datetime] = None

    numOrden:      Optional[str]     = None
    entregadoA:    Optional[str]     = None

    fechaCreacion:     Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None

    creadoPor:    Optional[str]     = None
    modificadoPor: Optional[str]     = None

    model_config = ConfigDict(from_attributes=True)
