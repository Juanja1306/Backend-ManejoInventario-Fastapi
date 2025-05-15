# app/routers/items.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import TblRoles, TblUsuario, TblEmpresas, TblUnidades, TblCategorias, TblUsuarioEmpresa, TblConsumos
from app.models import TblUsuarioCategoria, TblRepuestos, TblAuditoria, TblInventarios, TblAjustes, TblPeticiones, TblProductosPeticion

from typing import List, Optional
from datetime import datetime



from app.database import engine

router = APIRouter()


# Esquemas Pydantic de entrada
class UsuarioCreate(BaseModel):
    idUsuario: int
    correoUsuario: str
    rolcategoria: str
    modificadoPor: str

class EmpresaCreate(BaseModel):
    ruc: str
    nombre: str
    nombre_corto: str
    appsigiii: int


# Endpoint para crear un usuario
@router.post("/usuarios/", response_model=UsuarioCreate, status_code=201)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    db_usuario = TblUsuario(**usuario.dict())
    db.add(db_usuario)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=str(e))
    db.refresh(db_usuario)
    return db_usuario


# Endpoint para crear una empresa
@router.post("/empresas/", response_model=EmpresaCreate, status_code=201)
def create_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    db_empresa = TblEmpresas(**empresa.dict())
    db.add(db_empresa)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(400, detail=str(e))
    db.refresh(db_empresa)
    return db_empresa


# Endpoint para auditoría
class AuditoriaRead(BaseModel):
    idAuditoria: int
    empresa: str
    rucEmpresa: str
    categoria: str
    producto: str
    descripcion: Optional[str] = None
    unidadMedida: Optional[str] = None
    costoTotal: Optional[float] = None
    cantidad: Optional[float] = None
    motivo: Optional[str] = None
    comentarios: Optional[str] = None
    saldoInicial: Optional[float] = None
    saldoFinal: Optional[float] = None
    fechaSolicitada: Optional[datetime] = None
    fechaProcesada: Optional[datetime] = None
    numOrden: Optional[str] = None
    entregadoA: Optional[str] = None
    fechaCreacion: Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None
    creadoPor: Optional[str] = None
    modificadoPor: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# Endpoint para leer auditoría
@router.get("/auditoria/", response_model=List[AuditoriaRead], tags=["SIGII"])
def read_auditoria(db = Depends(get_db)):
    return db.query(TblAuditoria).all()



@router.get("/pool-status")
def pool_status():
    # engine.pool.status() devuelve algo como "Pool size: 10  Connections in pool: 9
    return {"odbc_pool": engine.pool.status()}








# Repetir el mismo patrón:
#    - Define un BaseModel con los campos de la tabla (por ejemplo TblUnidades, TblCategorias…)
#    - Crea un POST endpoint que: 
#         a) reciba ese Pydantic schema, 
#         b) haga db.add(model(**.dict())), 
#         c) db.commit(), 
#         d) db.refresh() y 
#         e) devuelva la instancia.
