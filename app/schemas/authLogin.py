from pydantic import BaseModel, Field, ConfigDict, EmailStr
from uuid import UUID
from datetime import datetime
from re import search

class AuthLoginSerializer(BaseModel):
    email: EmailStr
    password:str
    
class AuthLoginDeserializer(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    nombres: str
    apellidos:str
    