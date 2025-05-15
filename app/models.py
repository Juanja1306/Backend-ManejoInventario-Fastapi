#app/models.py

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TblRoles(Base):
    __tablename__ = "tblRoles"
    idRoles = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(String(50), nullable=False)
    
class TblUsuario(Base):
    __tablename__ = "tblUsuario"
    idUsuario     = Column(Integer, primary_key=True, nullable=False)
    correoUsuario = Column(String(100))
    rolcategoria  = Column(String(50), ForeignKey("tblRoles.descripcion"))
    modificadoPor = Column(String(100))

class TblEmpresas(Base):
    __tablename__ = "tblEmpresas"
    ruc = Column(String(13), primary_key=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    nombre_corto = Column(String(200), nullable=False)
    appsigiii = Column(Integer)

class TblUnidades(Base):
    __tablename__ = "tblUnidades"
    idUnidad = Column(Integer, primary_key=True, nullable=False)
    unidad = Column(String)      # nvarchar sin longitud explícita
    descripcion = Column(String) # nvarchar sin longitud explícita
    clase = Column(String)       # nvarchar sin longitud explícita

class TblCategorias(Base):
    __tablename__ = "tblCategorias"
    idCategoria = Column(String(20), primary_key=True, nullable=False)
    nombreCategoria = Column(String(50), nullable=False)

class TblUsuarioEmpresa(Base):
    __tablename__ = "tblUsuarioEmpresa"
    idAutoincrement = Column(Integer, primary_key=True, nullable=False)
    idUsuario       = Column(Integer, ForeignKey("tblUsuario.idUsuario"), nullable=False)
    ruc             = Column(String(13), ForeignKey("tblEmpresas.ruc"), nullable=False)

class TblUsuarioCategoria(Base):
    __tablename__ = "tblUsuarioCategoria"
    idAutoincrement = Column(Integer, primary_key=True, nullable=False)
    idUsuario       = Column(Integer, ForeignKey("tblUsuario.idUsuario"), nullable=False)
    idCategoria     = Column(String(20), ForeignKey("tblCategorias.idCategoria"), nullable=False)

class TblRepuestos(Base):
    __tablename__ = "tblRepuestos"
    codRepuesto = Column(String(50), primary_key=True, nullable=False)
    codJDE = Column(String(50))
    codFusion = Column(String(50))
    descripcion = Column(String)
    unidadMedida = Column(String(50), ForeignKey("tblUnidades.unidad"))
    costoUnitario = Column(Float)
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String)
    modificadoPor = Column(String)
    
class TblAuditoria(Base):
    __tablename__ = "tblAuditoria_bck"
    idAuditoria = Column(Integer, primary_key=True, nullable=False)
    empresa = Column(String(60), ForeignKey("tblEmpresas.nombre_corto"))
    rucEmpresa = Column(String(13), ForeignKey("tblEmpresas.ruc"))
    categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"))
    producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"))
    descripcion = Column(String(200))
    unidadMedida = Column(String(20), ForeignKey("tblUnidades.unidad"))
    costoTotal = Column(Float)
    cantidad = Column(Float)
    motivo = Column(String(100))
    comentarios = Column(String(300))
    saldoInicial = Column(Float)
    saldoFinal = Column(Float)
    fechaSolicitada = Column(DateTime)
    fechaProcesada = Column(DateTime)
    numOrden = Column(String(20))
    entregadoA = Column(String(100))
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String(100))
    modificadoPor = Column(String(100))

class TblInventarios(Base):
    __tablename__ = "tblInventarios_bck"
    idInventario = Column(Integer, primary_key=True, nullable=False)
    empresa = Column(String(50), ForeignKey("tblEmpresas.nombre_corto"))
    rucEmpresa = Column(String, ForeignKey("tblEmpresas.ruc"))
    categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"))
    producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"))
    descripcion = Column(String)
    cantidad = Column(Float)
    costoUnitario = Column(Float)
    costoTotal = Column(Float)
    unidadMedida = Column(String(50), ForeignKey("tblUnidades.unidad"))
    numOrden = Column(String(50))
    solicitadoPor = Column(String)
    ubicacion = Column(String(50))
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String(50))
    modificadoPor = Column(String(50))

class TblAjustes(Base):
    __tablename__ = "tblAjustes_bck"
    idAjuste = Column(Integer, primary_key=True, nullable=False)
    producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"))
    categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"))
    ajuste = Column(Float)
    motivo = Column(String)
    estado = Column(String(50))
    empresa = Column(String(50), ForeignKey("tblEmpresas.nombre_corto"))
    rucEmpresa = Column(String(50), ForeignKey("tblEmpresas.ruc"))
    estadoAnalista = Column(String(50))
    comentarioGerencia = Column(String)
    comentarioAnalista = Column(String)
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String(50))
    modificadoPor = Column(String(50))
    codigoInventario = Column(Integer, ForeignKey("tblInventarios.idInventario"))

class TblPeticiones(Base):
    __tablename__ = "tblPeticiones_bck"
    idPeticion = Column(Integer, primary_key=True, nullable=False)
    solicitante = Column(String(100))
    categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"))
    estado = Column(String(50))
    empresa = Column(String(60), ForeignKey("tblEmpresas.nombre_corto"))
    rucEmpresa = Column(String(13), ForeignKey("tblEmpresas.ruc"))
    fecha = Column(DateTime)
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String(100))
    modificadoPor = Column(String(100))

class TblProductosPeticion(Base):
    __tablename__ = "tblProductosPeticion_bck"
    idPeticionProducto = Column(Integer, primary_key=True, nullable=False)
    idPeticion = Column(Integer, ForeignKey("tblPeticiones.idPeticion"))
    idInventario = Column(Integer, ForeignKey("tblInventarios.idInventario"))
    producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"))
    cantidad = Column(Float)
    estado = Column(String(50))
    comentario = Column(String(300))
    procesado = Column(String(5))
    numOrden = Column(String(300))
    entregadoA = Column(String(100))
    solicitadaEntregada = Column(Integer)
    cantidadProcesada = Column(Float)
    fechaAtendida = Column(Date)
    fechaCreacion = Column(DateTime)
    fechaModificacion = Column(DateTime)
    creadoPor = Column(String(100))
    modificadoPor = Column(String(100))

class TblConsumos(Base):
    __tablename__ = "tblConsumos_bck"
    Id = Column(Integer, primary_key=True, nullable=False)
    FechaDato = Column(Date)
    PeriodoConsumo = Column(String(50))
    RazonSocial2 = Column(String(40))
    Articulo = Column(String(30))
    Consumos = Column(Float)
    MovimientoMeses = Column(Float)
    Activo1 = Column(String(30))
    DescripcionActivo1 = Column(String(255))
    Activo2 = Column(String(30))
    DescripcionActivo2 = Column(String(255))
    Activo3 = Column(String(30))
    DescripcionActivo3 = Column(String(255))
    Opcion1 = Column(String(1))
    Opcion2 = Column(String(1))
    Opcion3 = Column(String(1))
