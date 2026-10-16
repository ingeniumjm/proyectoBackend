from pydantic import BaseModel, Field , ConfigDict
from uuid import UUID
from datetime import datetime

class PaisesSerializer(BaseModel):
    # Serializador : Valida la data que llega de afuera (POST/PUT)
    codigo: str
    nombre: str
    
class PaisesDeserializer(BaseModel):
    # Deserializador : Transforma el objeto ORM a dict/JSON
    model_config = ConfigDict(from_attributes=True)

    codigo: str
    nombre: str