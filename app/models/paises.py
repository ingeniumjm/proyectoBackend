from sqlalchemy import Column, CHAR, String
from sqlalchemy.orm import relationship

from ..extensions import db


class Pais(db.Model):
    __tablename__ = "pais"

    codigo = Column(CHAR(2), primary_key=True)
    nombre = Column(String(100), nullable=False)

    clientes = relationship("Cliente", back_populates="pais")
