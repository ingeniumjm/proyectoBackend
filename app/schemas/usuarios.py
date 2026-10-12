from pydantic import BaseModel, Field, ConfigDict,EmailStr
from uuid import UUID
from datetime import datetime


class UsuarioSerializer(BaseModel):
    # Serializador : Es el encargado de validar la data que llega de afuera y verificar si es correcta
    nombres: str = Field(min_length=1, max_length=100, examples=["Juan Manuel"])
    apellidos: str = Field(min_length=1, max_length=100, examples=["Vásquez Callo"])
    email: EmailStr = Field(max_length=254, examples=["juan.vasquez@ingenium.pe"])
    telefono: str | None = Field(default=None, min_length=1, max_length=20)
    estado: str = Field(pattern="^(activo|bloqueado|inactivo)$")


class UsuarioDeserializer(BaseModel):
    # Deserializador : Transforma la data del modelo ORM a dict/JSON
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nombres: str
    apellidos: str
    email: str
    telefono: str | None
    estado: str
    email_verificado_en: datetime | None
    ultimo_acceso_en: datetime | None
    creado_en: datetime
    actualizado_en: datetime

