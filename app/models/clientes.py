import uuid

from sqlalchemy import (Column, String, CHAR, Integer, Text, DateTime, CheckConstraint,
                        UniqueConstraint, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..extensions import db
from .base import ahora

# Las funciones se pasan sin paréntesis, para ejecutarlas en cada inserción o actualización. Estos valores se calculan cuando SQLAlchemy ejecuta la operación, no necesariamente al construir el objeto.
# onupdate funciona para actualizaciones realizadas mediante SQLAlchemy; una actualización SQL directa no actualizará esa fecha automáticamente.

class Cliente(db.Model):
    __tablename__ = "cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pais_codigo = Column(CHAR(2), ForeignKey("pais.codigo"), nullable=False)
    tipo_documento = Column(String(20))
    numero_documento = Column(String(30))
    razon_social = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    estado = Column(String(20), nullable=False, default="registrado")
    zona_horaria = Column(String(64), nullable=False)
    limite_usuarios = Column(Integer, nullable=False, default=3)
    observaciones = Column(Text)
    creado_en = Column(DateTime(timezone=True), nullable=False, default=ahora)
    actualizado_en = Column(DateTime(timezone=True), nullable=False,
                            default=ahora, onupdate=ahora)

# __table_args__ es un atributo especial de SQLAlchemy donde se declaran restricciones , se colocan como tupla y SQLAlchemy lo interpreta al crear la tabla en la base de datos

# UniqueConstraint("pais_codigo", "tipo_documento", "numero_documento", name="uq_cliente_documento")
# Crea un indice unico compuesto: la combinacion de esos 3 campos no puede repetirse. Equivale al indexes.

# CheckConstraint(...) — son validaciones que PostgreSQL aplica dentro de la tabla:
# - ck_cliente_documento: tipo y número de documento van ambos vacíos (NULL) o ambos con valor; impide que quede uno sí y otro no.
# - ck_cliente_cupo: limite_usuarios no puede ser negativo.
# - ck_cliente_estado: estado solo puede ser uno de los 4 valores aprobados

# Siempre deben llevar un name para que se pueda identificar el error 

    __table_args__ = (
        UniqueConstraint("pais_codigo", "tipo_documento", "numero_documento",
                         name="uq_cliente_documento"),
        CheckConstraint(
            "(tipo_documento IS NULL AND numero_documento IS NULL) OR "
            "(tipo_documento IS NOT NULL AND numero_documento IS NOT NULL "
            "AND length(trim(tipo_documento)) > 0 AND length(trim(numero_documento)) > 0)",
            name="ck_cliente_documento",
        ),
        CheckConstraint("limite_usuarios >= 0", name="ck_cliente_cupo"),
        CheckConstraint(
            "estado IN ('registrado', 'activo', 'suspendido', 'inactivo')", name="ck_cliente_estado"),
    )


# Para las relaciones usamos back_populates para que esten en ambos archivos  y no olvidarme que existe una relacion ya que existe en ambos archivos

    pais = relationship("Pais", back_populates="clientes")
    vinculaciones = relationship("ClienteUsuario", back_populates="cliente")
    invitaciones = relationship("InvitacionCliente", back_populates="cliente")
    asignaciones = relationship("AsignacionControlador", back_populates="cliente")
    
#trim sirve para quitar los espacios 