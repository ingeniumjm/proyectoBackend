import uuid

from sqlalchemy import Column, String, Text, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class Permiso(db.Model):
    __tablename__ = "permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    ambito = Column(String(20), nullable=False)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    __table_args__ = (
        UniqueConstraint("codigo", name="uq_permiso_codigo"),
        CheckConstraint("ambito IN ('global', 'cliente')", name="ck_permiso_ambito"),
    )

    roles = relationship("RolPermiso", back_populates="permiso")
