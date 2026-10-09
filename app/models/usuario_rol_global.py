from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class UsuarioRolGlobal(db.Model):
    __tablename__ = "usuario_rol_global"

    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), primary_key=True)
    rol_id = Column(UUID(as_uuid=True), ForeignKey("rol.id"), primary_key=True)
    asignado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="roles_globales")
    rol = relationship("Rol", back_populates="asignaciones_globales")
    asignado_por_usuario = relationship("Usuario", foreign_keys=[asignado_por],
                                        back_populates="roles_globales_asignados")
