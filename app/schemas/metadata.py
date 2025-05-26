# metadata.py
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator
from datetime import datetime
from typing import List, Dict, Optional

class MetadataRead(BaseModel):
    idMetadata: int
    idUsuario: int
    idRol: int
    idAplicacion: int
    idEmpresa: int
    fechaCreacion: datetime

    # Permite leer atributos directamente desde el modelo SQLAlchemy
    model_config = ConfigDict(from_attributes=True)