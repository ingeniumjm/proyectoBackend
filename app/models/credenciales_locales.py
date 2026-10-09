from sqlalchemy import Column, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class CredencialLocal(db.Model):
    __tablename__ = "credencial_local"

    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), primary_key=True)
    password_hash = Column(Text, nullable=False)
    password_actualizado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    usuario = relationship("Usuario", back_populates="credencial")
