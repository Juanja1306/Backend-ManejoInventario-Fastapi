from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Type, Any

from app.database import get_db, engine
from app.models import (
    TblRoles, TblUsuario, TblEmpresas, TblUnidades, TblCategorias,
    TblUsuarioEmpresa, TblUsuarioCategoria, TblRepuestos,
    TblInventarios, TblAjustes, TblPeticiones,
    TblProductosPeticion, TblAuditoria
)

from app.schemas.roles             import RolSchema
from app.schemas.usuario           import UsuarioSchema
from app.schemas.empresa           import EmpresaSchema
from app.schemas.unidades          import UnidadSchema
from app.schemas.categorias        import CategoriaSchema
from app.schemas.usuario_empresa   import UsuarioEmpresaSchema
from app.schemas.usuario_categoria import UsuarioCategoriaSchema
from app.schemas.repuestos         import RepuestoSchema
from app.schemas.inventarios       import InventarioSchema
from app.schemas.ajustes           import AjusteSchema
from app.schemas.peticiones        import PeticionSchema
from app.schemas.productos_peticion import ProductoPeticionSchema
from app.schemas.auditoria         import AuditoriaSchema

router = APIRouter()

# Helper to register create endpoints
def register_create(prefix: str, model: Type[Any], schema: Type[Any]) -> None:
    @router.post(f"/{prefix}/", response_model=schema, status_code=201)
    def create_item(item: schema, db: Session = Depends(get_db)):
        db_obj = model(**item.dict(exclude_unset=True))
        db.add(db_obj)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(400, detail=str(e))
        db.refresh(db_obj)
        return db_obj

# Helper to register read endpoints
def register_read(prefix: str, model: Type[Any], schema: Type[Any]) -> None:
    @router.get(f"/{prefix}/", response_model=List[schema])
    def read_items(db: Session = Depends(get_db)):
        return db.query(model).all()

# Register create endpoints
entities_create = [
    ("roles", TblRoles, RolSchema),
    ("usuarios", TblUsuario, UsuarioSchema),
    ("empresas", TblEmpresas, EmpresaSchema),
    ("unidades", TblUnidades, UnidadSchema),
    ("categorias", TblCategorias, CategoriaSchema),
    ("usuario-empresas", TblUsuarioEmpresa, UsuarioEmpresaSchema),
    ("usuario-categorias", TblUsuarioCategoria, UsuarioCategoriaSchema),
    ("repuestos", TblRepuestos, RepuestoSchema),
    ("inventarios", TblInventarios, InventarioSchema),
    ("ajustes", TblAjustes, AjusteSchema),
    ("peticiones", TblPeticiones, PeticionSchema),
    ("productos-peticion", TblProductosPeticion, ProductoPeticionSchema),
]
for prefix, model, schema in entities_create:
    register_create(prefix, model, schema)

# Register read endpoints
entities_read = [
    ("roles", TblRoles, RolSchema),
    ("auditoria", TblAuditoria, AuditoriaSchema)
]
for prefix, model, schema in entities_read:
    register_read(prefix, model, schema)

# Pool status endpoint
@router.get("/pool-status")
def pool_status():
    return {"odbc_pool": engine.pool.status()}
