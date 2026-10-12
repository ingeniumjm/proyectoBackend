from pydantic import BaseModel, Field, ConfigDict, field_validator
from uuid import UUID
from datetime import datetime
from re import search

class CredencialesLocalesSerializer(BaseModel):
    # Valida la data que llega de afuera (POST/PUT)
    usuario_id: UUID
    password_hash: str = Field(max_length=128)

    @field_validator("password_hash")
    def validar_password(cls, valor):
        errores = []

    # Expresiones Regulares (REGEX) es una forma de validar si un texto cumple o no con determinadas reglas sin importar su contenido, es decir, al menos una mayus, al menos una minus, al menos un numero, al menos un caractyer especial
        if len(valor) < 8:
            errores.append("El password no debe ser menor a 8 caracteres")

        if not search(r"[A-Z]", valor):
            errores.append("Falta una mayuscula")
        if not search(r"[a-z]", valor):
            errores.append("Falta una minuscula")
        if not search(r"\d", valor):
            errores.append("Falta un numero")
        if not search(r"[^A-Za-z0-9]", valor):
            errores.append("Falta un caracter especial")
        if errores:
            raise ValueError(",".join(errores))
        return valor


class CredencialesLocalesDeserializer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_id: UUID
    password_hash: str
    password_actualizado_en: datetime
    creado_en: datetime
    actualizado_en: datetime
