from pydantic import BaseModel, ConfigDict

class EmpresaSchema(BaseModel):
    ruc: str               # PK obligatorio
    nombre: str
    nombre_corto: str
    appsigiii: int

    model_config = ConfigDict(from_attributes=True)
