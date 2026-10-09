import uuid

from sqlalchemy import Column, String, Text, DateTime, CheckConstraint, Index, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class InvitacionCliente(db.Model):
    __tablename__ = "invitacion_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("cliente.id"), nullable=False)
    email = Column(String(254), nullable=False)
    invitado_por = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    estado = Column(String(20), nullable=False, default="pendiente")
    token_hash = Column(Text, nullable=False)
    vence_en = Column(DateTime(timezone=True), nullable=False)
    aceptada_en = Column(DateTime(timezone=True))
    cliente_usuario_id = Column(UUID(as_uuid=True), ForeignKey("cliente_usuario.id"))
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'aceptada', 'cancelada', 'vencida')",
                        name="ck_invitacion_estado"),
        CheckConstraint("vence_en > creado_en", name="ck_invitacion_vigencia"),
        CheckConstraint(
            "(estado = 'aceptada' AND aceptada_en IS NOT NULL AND cliente_usuario_id IS NOT NULL) "
            "OR (estado <> 'aceptada' AND aceptada_en IS NULL AND cliente_usuario_id IS NULL)",
            name="ck_invitacion_aceptacion",
        ),
        Index("uq_invitacion_pendiente_ci", "cliente_id", func.lower(email),
              unique=True, postgresql_where=(estado == "pendiente")),
    )

    cliente = relationship("Cliente", back_populates="invitaciones")
    invitado_por_usuario = relationship("Usuario", back_populates="invitaciones_invitadas")
    cliente_usuario = relationship("ClienteUsuario", back_populates="invitaciones")
    roles = relationship("InvitacionClienteRol", back_populates="invitacion")
