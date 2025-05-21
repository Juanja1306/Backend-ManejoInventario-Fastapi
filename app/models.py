# #app/models.py

# from sqlalchemy import (
#     Column, Integer, String, Float, DateTime, Date, ForeignKey
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship

# Base = declarative_base()

# Unicas -------------------------------------

# class TblUnidades(Base):
#     __tablename__ = "tblUnidades"

#     idUnidad = Column(Integer, primary_key=True, nullable=False)
#     unidad = Column(String, nullable=False)
#     descripcion = Column(String, nullable=False)
#     clase = Column(String, nullable=False)

#     # Relaciones
#     repuestos = relationship("TblRepuestos", back_populates="unidad_medida_rel")
#     inventarios = relationship("TblInventarios", back_populates="unidad_medida_rel")
#     auditorias = relationship("TblAuditoria", back_populates="unidad_medida_rel")
    
# class TblCategorias(Base):
#     __tablename__ = "tblCategorias"

#     idCategoria = Column(String(20), primary_key=True, nullable=False)
#     nombreCategoria = Column(String(50), nullable=False)

#     peticiones = relationship("TblPeticiones", back_populates="categoria_rel")
#     auditorias = relationship("TblAuditoria", back_populates="categoria_rel")
#     inventarios = relationship("TblInventarios", back_populates="categoria_rel")

# class TblUsuarioOrganizacion(Base):
#     __tablename__ = "tblUsuarioOrganizacion"

#     idAutoincrement = Column(Integer, primary_key=True, nullable=False)
#     correoUsuario = Column(String(100), nullable=False)
#     codOrg = Column(Integer, ForeignKey("tblOrganizacionInventario.codOrg"), nullable=False)

#     organizacion_rel = relationship("TblOrganizacionInventario", back_populates="usuario_organizaciones")
    
# class TblMotivo(Base):
#     __tablename__ = "tblMotivo"

#     idMotivo = Column(Integer, primary_key=True, nullable=False)
#     descripcion = Column(String(50), nullable=False)

#     auditorias = relationship("TblAuditoria", back_populates="motivo_rel")
#     ajustes = relationship("TblAjustes", back_populates="motivo_rel")
    
# class TblEstado(Base):
#     __tablename__ = "tblEstado"

#     idEstado = Column(Integer, primary_key=True, nullable=False)
#     descripcion = Column(String(50), nullable=False)

#     peticiones = relationship("TblPeticiones", back_populates="estado_rel")
#     productos_peticiones = relationship("TblProductosPeticion", back_populates="estado_rel")
#     ajustes = relationship("TblAjustes", back_populates="estado_analista_rel")
    
# class TblRepuestos(Base):
#     __tablename__ = "tblRepuestos"

#     codRepuesto = Column(String(50), primary_key=True, nullable=False)
#     codJDE = Column(String(50))
#     codFusion = Column(String(50))
#     descripcion = Column(String)
#     unidadMedida = Column(String(50), ForeignKey("tblUnidades.unidad"), nullable=False)
#     costoUnitario = Column(Float, nullable=False)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     unidad_medida_rel = relationship("TblUnidades", back_populates="repuestos")
#     productos_peticiones = relationship("TblProductosPeticion", back_populates="producto_rel")
#     auditorias = relationship("TblAuditoria", back_populates="producto_rel")
#     inventarios = relationship("TblInventarios", back_populates="producto_rel")
#     ajustes = relationship("TblAjustes", back_populates="producto_rel")
    
# # Dependientes -------------------------------------

# class TblUsuarioEmpresa(Base):
#     __tablename__ = "tblUsuarioEmpresa"

#     idAutoincrement = Column(Integer, primary_key=True, nullable=False)
#     correoUsuario = Column(String(100), nullable=False)
#     ruc = Column(String(13), ForeignKey("tblEmpresas.ruc"), nullable=False)

#     empresa_rel = relationship("TblEmpresas", back_populates="usuario_empresas")

# class TblOrganizacionInventario(Base):
#     __tablename__ = "tblOrganizacionInventario"

#     codOrg = Column(Integer, primary_key=True, nullable=False)
#     empresa = Column(String(200), ForeignKey("tblEmpresas.nombre_corto"), nullable=False)
#     nombreOrg = Column(String(100), nullable=False)

#     empresa_rel = relationship("TblEmpresas", back_populates="inventarios")
#     inventarios = relationship("TblInventarios", back_populates="organizacion_rel")
    
# class TblAuditoria(Base):
#     __tablename__ = "tblAuditoria"

#     idAuditoria = Column(Integer, primary_key=True, nullable=False)
#     empresa = Column(String(200), ForeignKey("tblEmpresas.nombre_corto"), nullable=False)
#     rucEmpresa = Column(String(13), ForeignKey("tblEmpresas.ruc"), nullable=False)
#     categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"), nullable=False)
#     producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"), nullable=False)
#     motivo = Column(String(50), ForeignKey("tblMotivo.descripcion"), nullable=False)
#     unidadMedida = Column(String(20), ForeignKey("tblUnidades.unidad"), nullable=False)
#     descripcion = Column(String(200))
#     costoTotal = Column(Float, nullable=False)
#     cantidad = Column(Float, nullable=False)
#     comentarios = Column(String(300))
#     saldoInicial = Column(Float)
#     saldoFinal = Column(Float)
#     fechaSolicitada = Column(DateTime, nullable=False)
#     fechaProcesada = Column(DateTime)
#     numOrden = Column(String(20))
#     entregadoA = Column(String(100), nullable=False)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     empresa_rel = relationship("TblEmpresas", back_populates="auditorias")
#     categoria_rel = relationship("TblCategorias", back_populates="auditorias")
#     producto_rel = relationship("TblRepuestos", back_populates="auditorias")
#     motivo_rel = relationship("TblMotivo", back_populates="auditorias")
#     unidad_medida_rel = relationship("TblUnidades", back_populates="auditorias")

# class TblInventarios(Base):
#     __tablename__ = "tblInventarios"

#     idInventario = Column(Integer, primary_key=True, nullable=False)
#     empresa = Column(String(200), ForeignKey("tblEmpresas.nombre_corto"), nullable=False)
#     rucEmpresa = Column(String, ForeignKey("tblEmpresas.ruc"), nullable=False)
#     categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"), nullable=False)
#     producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"), nullable=False)
#     codOrg = Column(Integer, ForeignKey("tblOrganizacionInventario.codOrg"), nullable=False)
#     descripcion = Column(String)
#     cantidad = Column(Float, nullable=False)
#     costoUnitario = Column(Float, nullable=False)
#     costoTotal = Column(Float, nullable=False)
#     unidadMedida = Column(String(50), ForeignKey("tblUnidades.unidad"))
#     numOrden = Column(String(50))
#     solicitadoPor = Column(String(100))
#     ubicacion = Column(String(50), nullable=False)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     empresa_rel = relationship("TblEmpresas", back_populates="inventarios")
#     categoria_rel = relationship("TblCategorias", back_populates="inventarios")
#     producto_rel = relationship("TblRepuestos", back_populates="inventarios")
#     organizacion_rel = relationship("TblOrganizacionInventario", back_populates="inventarios")
#     unidad_medida_rel = relationship("TblUnidades", back_populates="inventarios")
#     productos_peticiones = relationship("TblProductosPeticion", back_populates="inventario_rel")

# class TblAjustes(Base):
#     __tablename__ = "tblAjustes"

#     idAjuste = Column(Integer, primary_key=True, nullable=False)
#     producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"), nullable=False)
#     categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"), nullable=False)
#     codigoInventario = Column(Integer, ForeignKey("tblInventarios.idInventario"), nullable=False)
#     ajuste = Column(Float)
#     motivo = Column(String)
#     estado = Column(String(50), ForeignKey("tblMotivo.descripcion"))
#     empresa = Column(String(200), ForeignKey("tblEmpresas.nombre_corto"), nullable=False)
#     rucEmpresa = Column(String(50), ForeignKey("tblEmpresas.ruc"), nullable=False)
#     estadoAnalista = Column(String(50), ForeignKey("tblEstado.descripcion"))
#     comentarioGerencia = Column(String)
#     comentarioAnalista = Column(String)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     producto_rel = relationship("TblRepuestos", back_populates="ajustes")
#     categoria_rel = relationship("TblCategorias")
#     inventario_rel = relationship("TblInventarios")
#     motivo_rel = relationship("TblMotivo", back_populates="ajustes")
#     estado_analista_rel = relationship("TblEstado", back_populates="ajustes")
#     empresa_rel = relationship("TblEmpresas")

# class TblPeticiones(Base):
#     __tablename__ = "tblPeticiones"

#     idPeticion = Column(Integer, primary_key=True, nullable=False)
#     solicitante = Column(String(100))
#     categoria = Column(String(50), ForeignKey("tblCategorias.nombreCategoria"))
#     estado = Column(String(50), ForeignKey("tblEstado.descripcion"))
#     empresa = Column(String(200), ForeignKey("tblEmpresas.nombre_corto"))
#     rucEmpresa = Column(String(13), ForeignKey("tblEmpresas.ruc"))
#     fecha = Column(DateTime)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     categoria_rel = relationship("TblCategorias", back_populates="peticiones")
#     estado_rel = relationship("TblEstado", back_populates="peticiones")
#     empresa_rel = relationship("TblEmpresas", back_populates="peticiones")
#     produtos_rel = relationship("TblProductosPeticion", back_populates="peticion_rel")

# class TblProductosPeticion(Base):
#     __tablename__ = "tblProductosPeticion"

#     idPeticionProducto = Column(Integer, primary_key=True, nullable=False)
#     idPeticion = Column(Integer, ForeignKey("tblPeticiones.idPeticion"))
#     idInventario = Column(Integer, ForeignKey("tblInventarios.idInventario"))
#     producto = Column(String(50), ForeignKey("tblRepuestos.codRepuesto"))
#     cantidad = Column(Float, nullable=False)
#     estado = Column(String(50), ForeignKey("tblEstado.descripcion"))
#     comentario = Column(String(300))
#     procesado = Column(String(5))
#     numOrden = Column(String(300))
#     entregadoA = Column(String(100))
#     solicitadaEntregada = Column(Integer)
#     cantidadProcesada = Column(Float)
#     fechaAtendida = Column(Date)
#     fechaCreacion = Column(DateTime, nullable=False)
#     fechaModificacion = Column(DateTime, nullable=False)
#     creadoPor = Column(String(100), nullable=False)
#     modificadoPor = Column(String(100), nullable=False)

#     peticion_rel = relationship("TblPeticiones", back_populates="produtos_rel")
#     inventario_rel = relationship("TblInventarios", back_populates="productos_peticiones")
#     producto_rel = relationship("TblRepuestos", back_populates="productos_peticiones")
#     estado_rel = relationship("TblEstado", back_populates="productos_peticiones")
