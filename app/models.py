# #app/models.py

from sqlalchemy import Integer, String, ForeignKey, Float, DateTime, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime, date
from typing import List, Dict

Base = declarative_base()


# Unicas -------------------------------------

class Empresa(Base):
    __tablename__ = "tblEmpresas"
    __table_args__ = {"schema": "dbo"}

    ruc: Mapped[str] = mapped_column(String(13), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)

    organizaciones: Mapped[List["Organizacion"]] = relationship(
        "Organizacion", back_populates="empresa"
    )
    usuarios_empresas: Mapped[List["UsuarioEmpresa"]] = relationship(
        "UsuarioEmpresa", back_populates="empresa"
    )

class Zona(Base):
    __tablename__ = "tblZonas"
    __table_args__ = {"schema": "dbo"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), nullable=False)

    organizaciones: Mapped[List["Organizacion"]] = relationship(
        "Organizacion", back_populates="zona_rel"
    )

class Organizacion(Base):
    __tablename__ = "tblOrganizaciones"
    __table_args__ = {"schema": "dbo"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False  
    )
    codigo: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    nombre: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    ciudad: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
    ruc_empresa: Mapped[str] = mapped_column(
        String(13),
        ForeignKey("dbo.tblEmpresas.ruc"),
        nullable=True
    )
    zona: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("dbo.tblZonas.id"),
        nullable=True
    )
    nom_empresa: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )

    # Relaciones
    empresa: Mapped["Empresa"] = relationship(
        "Empresa",
        back_populates="organizaciones",
        foreign_keys=[ruc_empresa]
    )
    zona_rel: Mapped["Zona"] = relationship(
        "Zona",
        back_populates="organizaciones",
        foreign_keys=[zona]
    )

class Unidad(Base):
    __tablename__ = "tblUnidades"
    __table_args__ = {"schema": "dbo"}

    idUnidad: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=False
    )
    unidad: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    clase: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

# Dependientes -------------------------------------

class UsuarioOrganizacion(Base):
    __tablename__ = "tblUsuarioOrganizacion"
    __table_args__ = {"schema": "dbo"}  # Ajusta el esquema si es necesario

    idUsuarioOrganizacion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    correoUsuario: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    codOrg: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

class UsuarioEmpresa(Base):
    __tablename__ = "tblUsuarioEmpresa"
    __table_args__ = {"schema": "dbo"}

    idUsuarioEmpresa: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    correoUsuario: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    ruc: Mapped[str] = mapped_column(
        String(13),
        ForeignKey("dbo.tblEmpresas.ruc"),
        nullable=False
    )

    # Relación con Empresa (opcional, si existe el modelo Empresa)
    empresa: Mapped["Empresa"] = relationship(
        "Empresa",
        back_populates="usuarios_empresas",
        foreign_keys=[ruc]
    )

class Peticion(Base):
    __tablename__ = "tblPeticiones_bck"
    __table_args__ = {"schema": "dbo"}

    idPeticion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    solicitante: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    empresa: Mapped[str] = mapped_column(
        String(60),
        nullable=True
    )
    rucEmpresa: Mapped[str] = mapped_column(
        String(13),
        nullable=True
    )
    fecha: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaModificacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    creadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    modificadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

class ProductoPeticion(Base):
    __tablename__ = "tblProductosPeticion_bck"
    __table_args__ = {"schema": "dbo"}

    idPeticionProducto: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    idPeticion: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    idInventario: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    producto: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    cantidad: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    comentario: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )
    procesado: Mapped[str] = mapped_column(
        String(5),
        nullable=True
    )
    numOrden: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )
    entregadoA: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    solicitadaEntregada: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    cantidadProcesada: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    fechaAtendida: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaModificacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    creadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    modificadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

class Inventario(Base):
    __tablename__ = "tblInventarios_bck"
    __table_args__ = {"schema": "dbo"}

    idInventario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    empresa: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    rucEmpresa: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    producto: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    cantidad: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    costoUnitario: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    costoTotal: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    unidadMedida: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    numOrden: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    solicitadoPor: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    ubicacion: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaModificacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    creadoPor: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    modificadoPor: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

class Auditoria(Base):
    __tablename__ = "tblAuditoria_bck"
    __table_args__ = {"schema": "dbo"}

    idAuditoria: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    empresa: Mapped[str] = mapped_column(
        String(60),
        nullable=True
    )
    rucEmpresa: Mapped[str] = mapped_column(
        String(13),
        nullable=True
    )
    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    producto: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    descripcion: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )
    unidadMedida: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    costoTotal: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    cantidad: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    motivo: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    comentarios: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )
    saldoInicial: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    saldoFinal: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    fechaSolicitada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaProcesada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    numOrden: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )
    entregadoA: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaModificacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    creadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    modificadoPor: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

class Ajuste(Base):
    __tablename__ = "tblAjustes_bck"
    __table_args__ = {"schema": "dbo"}

    idAjuste: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    producto: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    categoria: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    ajuste: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    motivo: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    empresa: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    rucEmpresa: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    estadoAnalista: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    comentarioGerencia: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    comentarioAnalista: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    fechaModificacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )
    creadoPor: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    modificadoPor: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )
    codigoInventario: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
