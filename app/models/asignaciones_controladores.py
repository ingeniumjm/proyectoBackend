import uuid

from sqlalchemy import Column, Text, DateTime, CheckConstraint, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class AsignacionControlador(db.Model):
    __tablename__ = "asignacion_controlador"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    controlador_id = Column(UUID(as_uuid=True), ForeignKey("controlador.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("cliente.id"), nullable=False)
    asignado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    inicio_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    fin_en = Column(DateTime(timezone=True))
    finalizado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"))
    motivo_fin = Column(Text)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)

    __table_args__ = (
        CheckConstraint("fin_en IS NULL OR fin_en >= inicio_en", name="ck_asignacion_periodo"),
        Index("uq_controlador_asignacion_vigente", "controlador_id",
              unique=True, postgresql_where=(fin_en.is_(None))),
    )

    controlador = relationship("Controlador", back_populates="asignaciones")
    cliente = relationship("Cliente", back_populates="asignaciones")
    asignado_por_usuario = relationship("Usuario", foreign_keys=[asignado_por],
                                        back_populates="asignaciones_asignadas")
    finalizado_por_usuario = relationship("Usuario", foreign_keys=[finalizado_por],
                                          back_populates="asignaciones_finalizadas")
