import uuid

from sqlalchemy import Column, String, Text, DateTime, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class Controlador(db.Model):
    __tablename__ = "controlador"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_serie = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=False)
    version_hardware = Column(String(50))
    version_firmware = Column(String(50))
    estado = Column(String(20), nullable=False, default="inventario")
    aws_thing_name = Column(String(128))
    registrado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    observaciones = Column(Text)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    __table_args__ = (
        UniqueConstraint("numero_serie", name="uq_controlador_numero_serie"),
        UniqueConstraint("aws_thing_name", name="uq_controlador_aws_thing_name"),
        CheckConstraint(
            "estado IN ('inventario', 'habilitado', 'mantenimiento', 'retirado')",
            name="ck_controlador_estado",
        ),
    )

    registrado_por_usuario = relationship("Usuario",
                                          back_populates="controladores_registrados")
    asignaciones = relationship("AsignacionControlador", back_populates="controlador")
