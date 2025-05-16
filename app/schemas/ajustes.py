from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AjusteSchema(BaseModel):
    idAjuste: Optional[int] = None
    producto: str
    categoria: str
    ajuste: float
    motivo: str
    estado: str
    empresa: str
    rucEmpresa: str
    estadoAnalista: str
    comentarioGerencia: str
    comentarioAnalista: str
    fechaCreacion: datetime
    fechaModificacion: datetime
    creadoPor: str
    modificadoPor: str
    codigoInventario: int

    model_config = ConfigDict(from_attributes=True)
  