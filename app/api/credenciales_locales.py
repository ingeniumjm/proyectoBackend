from flask_restful import Resource, request
from app.models import CredencialLocal
from app.extensions import db
from app.schemas import CredencialesLocalesSerializer,CredencialesLocalesDeserializer
from pydantic import ValidationError
from bcrypt import gensalt, hashpw

class CredencialesLocalesController(Resource):
    def post(self):
        try:
            dataValidada= CredencialesLocalesSerializer.model_validate(request.get_json())

            #Proceso del hashing de la password
            # 1. Generamos el texto de ayuda (salt)
            salt = gensalt()
            # 2. Convertimos el passwoard a bytes
            password = dataValidada.password_hash.encode()
            # 3. Hacemos el hashing de la password
            password_hasheada_byte= hashpw(password,salt)
            # 4. Convertimos el hashing del password en bytes a str
            password_hasheada=password_hasheada_byte.decode()
            nuevaCredencialLocal=CredencialLocal(**dataValidada.model_dump(exclude={"password_hash"}),password_hash=password_hasheada)
            db.session.add(nuevaCredencialLocal)
            db.session.commit()

            return{
                "message": "Credencial registrada exitosamente"

            },201
        except ValidationError as error:
            return{
                "message": "Error al crear la credencial",
                "content": error.errors(include_context=False)
            },400    