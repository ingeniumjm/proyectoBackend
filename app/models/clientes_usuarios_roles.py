from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class ClienteUsuarioRol(db.Model):
    __tablename__ = "cliente_usuario_rol"

    cliente_usuario_id = Column(UUID(as_uuid=True), ForeignKey("cliente_usuario.id"), primary_key=True)
    rol_id = Column(UUID(as_uuid=True), ForeignKey("rol.id"), primary_key=True)
    asignado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)

    cliente_usuario = relationship("ClienteUsuario", back_populates="roles")
    rol = relationship("Rol", back_populates="asignaciones_cliente")
    asignado_por_usuario = relationship("Usuario", foreign_keys=[asignado_por],
                                        back_populates="roles_cliente_asignados")
