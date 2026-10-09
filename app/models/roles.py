import uuid

from sqlalchemy import Column, String, Text, Boolean, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class Rol(db.Model):
    __tablename__ = "rol"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    ambito = Column(String(20), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    __table_args__ = (
        UniqueConstraint("codigo", name="uq_rol_codigo"),
        CheckConstraint("ambito IN ('global', 'cliente')", name="ck_rol_ambito"),
    )

    permisos = relationship("RolPermiso", back_populates="rol")
    asignaciones_cliente = relationship("ClienteUsuarioRol", back_populates="rol")
    invitaciones = relationship("InvitacionClienteRol", back_populates="rol")
    asignaciones_globales = relationship("UsuarioRolGlobal", back_populates="rol")
