from pydantic import BaseModel, ConfigDict

class CategoriaSchema(BaseModel):
    idCategoria: str
    nombreCategoria: str

    model_config = ConfigDict(from_attributes=True)
