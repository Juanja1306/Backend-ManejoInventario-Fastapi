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