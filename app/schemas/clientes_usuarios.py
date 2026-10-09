from pydantic import BaseModel, Field , ConfigDict
from uuid import UUID
from datetime import datetime

class ClientesUsuariosSerializer(BaseModel):
    # Serializador : Valida la data que llega de afuera (POST/PUT)
    cliente_id: UUID
    usuario_id: UUID
    estado: str = Field(pattern="^(activo|inactivo)$")


class ClientesUsuariosDeserializer(BaseModel):
    # Deserializador : Transforma el objeto ORM a dict/JSON
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cliente_id: UUID
    usuario_id: UUID
    estado: str
    creado_en: datetime
    actualizado_en: datetime