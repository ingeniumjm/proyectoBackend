from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class InvitacionClienteRol(db.Model):
    __tablename__ = "invitacion_cliente_rol"

    invitacion_id = Column(UUID(as_uuid=True), ForeignKey("invitacion_cliente.id"), primary_key=True)
    rol_id = Column(UUID(as_uuid=True), ForeignKey("rol.id"), primary_key=True)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)

    invitacion = relationship("InvitacionCliente", back_populates="roles")
    rol = relationship("Rol", back_populates="invitaciones")
