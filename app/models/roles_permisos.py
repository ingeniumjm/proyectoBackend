from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class RolPermiso(db.Model):
    __tablename__ = "rol_permiso"

    rol_id = Column(UUID(as_uuid=True), ForeignKey("rol.id"), primary_key=True)
    permiso_id = Column(UUID(as_uuid=True), ForeignKey("permiso.id"), primary_key=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")
