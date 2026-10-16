import uuid

from sqlalchemy import Column, String, DateTime, CheckConstraint, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False)
    telefono = Column(String(20))
    estado = Column(String(20), nullable=False)
#******************************************************
    rol = Column(String(20), nullable=False)
#******************************************************
    email_verificado_en = Column(DateTime(timezone=True))
    ultimo_acceso_en = Column(DateTime(timezone=True))
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)


    __table_args__ = (
        CheckConstraint("estado IN ('activo', 'bloqueado', 'inactivo')",
                        name="ck_usuario_estado"),
        # Indice unico sobre lower(email): el correo no distingue mayusculas.
        # func.lower() se traduce a la funcion lower() de PostgreSQL.
        Index("uq_usuario_email_ci", func.lower(email), unique=True),
    )

    credencial = relationship(
        "CredencialLocal",
        back_populates="usuario",
        uselist=False
    )
    vinculaciones = relationship(
        "ClienteUsuario",
        back_populates="usuario"
    )
    invitaciones_invitadas = relationship(
        "InvitacionCliente",
        back_populates="invitado_por_usuario"
        )
    controladores_registrados = relationship(
        "Controlador",
        back_populates="registrado_por_usuario"
        )
    asignaciones_asignadas = relationship(
        "AsignacionControlador",
        foreign_keys="AsignacionControlador.asignado_por",
        back_populates="asignado_por_usuario",
    )
    asignaciones_finalizadas = relationship(
        "AsignacionControlador",
        foreign_keys="AsignacionControlador.finalizado_por",
        back_populates="finalizado_por_usuario",
    )
    roles_globales = relationship(
        "UsuarioRolGlobal",
        foreign_keys="UsuarioRolGlobal.usuario_id",
        back_populates="usuario",
    )
    roles_globales_asignados = relationship(
        "UsuarioRolGlobal",
        foreign_keys="UsuarioRolGlobal.asignado_por",
        back_populates="asignado_por_usuario",
    )
    roles_cliente_asignados = relationship(
        "ClienteUsuarioRol",
        foreign_keys="ClienteUsuarioRol.asignado_por",
        back_populates="asignado_por_usuario",
    )
