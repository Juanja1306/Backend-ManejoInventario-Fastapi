from pydantic import BaseModel

class OrganizacionRead(BaseModel):
    nombre: str

    class Config:
        json_schema_extra = {
            "example": {"nombre": "ORG001"}
        }

class CodigoOrganizacion(BaseModel):
    nombre: str

    class Config:
        json_schema_extra = {
            "example": {"codigo": "ORG001"}
        }

class UsuarioOrganizacionCreate(BaseModel):
    correo: str
    codigo: str

    class Config:
        json_schema_extra = {
            "example": {"correo": "user@example.com", "codigo": "ORG001"}
        }