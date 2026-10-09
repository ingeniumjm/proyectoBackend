import uuid

from sqlalchemy import Column, String, DateTime, CheckConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class ClienteUsuario(db.Model):
    __tablename__ = "cliente_usuario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("cliente.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    estado = Column(String(20), nullable=False)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

    __table_args__ = (
        # Una unica vinculacion por par cliente-usuario.
        UniqueConstraint("cliente_id", "usuario_id", name="uq_cliente_usuario"),
        CheckConstraint("estado IN ('activo', 'inactivo')",
                        name="ck_cliente_usuario_estado"),
    )

    cliente = relationship("Cliente", back_populates="vinculaciones")
    usuario = relationship("Usuario", back_populates="vinculaciones")
    roles = relationship("ClienteUsuarioRol", back_populates="cliente_usuario")
    invitaciones = relationship("InvitacionCliente", back_populates="cliente_usuario")
