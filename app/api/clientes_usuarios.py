# Ahora todos los metodos(GET, POST, PUT, DELETE) se definiran como metodos de una clase
from flask_restful import Resource, request

# importamos ClienteSerializar
from app.schemas import ClientesUsuariosSerializer, ClientesUsuariosDeserializer
from pydantic import ValidationError, TypeAdapter
from app.models import ClienteUsuario
from app.extensions import db

class ClientesUsuariosController(Resource):

    def post(self):
        try:
            dataValidada= ClientesUsuariosSerializer.model_validate(request.get_json())
            return{
                "message": "Usuarios agregada a los clientes"
            }
        except ValidationError as error:
            return {
                "message" : "Error al crear las categorias del libro",
                "content" : error.errors()
            }
