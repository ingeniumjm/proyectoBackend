from pydantic import BaseModel, Field , ConfigDict
from uuid import UUID
from datetime import datetime

# pydantic valida la lconfiguracion que nosotros definamos en los atributos de la clase, es decir, utilizara la configuracion de cada atriburo para que cuando le pasemos la informacion esta sea corroborada y si se valida, continuara, sino emitira un error de validacion
class ClienteSerializer(BaseModel):
    #Serializador :  Es el encargado de validar la data que llega de afuera y verificar si es correcta
    razon_social: str= Field(examples=["Quenixtech", "Municipalidad de Lima"])
    pais_codigo: str= Field(min_length=2, max_length=2, examples=["PE"])
    zona_horaria: str= Field(examples=["America/Lima"])
    tipo_documento: str | None = Field(default=None, min_length=1, max_length=20)
    numero_documento: str | None = Field(default=None, min_length=1, max_length=30)
    nombre_comercial: str | None = Field(default=None, max_length=200)
    estado: str = Field(default="registrado", pattern="^(registrado|activo|suspendido|inactivo)$")
    limite_usuarios: int = Field(default=3, ge=0)
    observaciones: str | None = None



class ClienteDeserializer(BaseModel):
    # Deserializador :  Transformar la data proveniente de mi entorno (python) y devolvera en un formato legible (dict | json)
    # model_config es un atributo propio de la clase BaseModel que sirve para modificar todo el modelo en su totalidad, y no solamente un solo atributo
    # ConfigDict > sirve par indicar que la informacion que vamos a pasarle a este deserializador se realizara en formato de instancias y no en formato de un dict
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    razon_social: str
    pais_codigo: str
    tipo_documento: str | None
    numero_documento: str | None
    nombre_comercial: str | None
    estado: str
    zona_horaria: str
    limite_usuarios: int
    observaciones: str | None
    creado_en: datetime
    actualizado_en: datetime