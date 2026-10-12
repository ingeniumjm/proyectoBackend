from flask_restful import Resource, request
from app.extensions import db
from pydantic import ValidationError
from bcrypt import gensalt, hashpw,checkpw
from app.schemas import AuthLoginSerializer,AuthLoginDeserializer
from app.models import Usuario,CredencialLocal
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from os import getenv
from datetime import timedelta

class AuthLoginController(Resource):

    def post(self):
        try:
            dataValidada = AuthLoginSerializer.model_validate(request.get_json())
            usuarioEncontrado=db.session.query(Usuario).filter(Usuario.email==dataValidada.email).first()
            if not usuarioEncontrado:
                return{
                    "message":"usuario no existe"
                },404
            password= dataValidada.password.encode()

            passwordEncontrado=db.session.query(CredencialLocal).filter(CredencialLocal.usuario_id==usuarioEncontrado.id).first()

            hashedPassword=passwordEncontrado.password_hash.encode()

            # check sirve para que usando el hashing almacenado en la bd me diga si es o no es la password sin la necesidad de saber el valor inicial
            esLaPasword= checkpw(password,hashedPassword)
            if esLaPasword:
                jwt=create_access_token(identity=usuarioEncontrado.id,# Es el identificador de la jwt, a quien le pertenece
                                        fresh=False, # Si queremos que esta JWT sea usada como un refresh jwt
                                        expires_delta=timedelta(hours=8,minutes=5)) # Indica la duracion que tendra de validez esta JWT
                return {
                    "message":"Bienvenido",
                    "content":jwt
                }
            else:
                return{
                    "message": "credenciales incorrectas"

                },400    


        except ValidationError as error:
            return{
                "message":"Error al hacer el login",
                "content": error.errors(include_context=False)
            }

class UserController(Resource):
    @jwt_required() # sirve para indicar que el metodo que va a tratar de acceder tenga que enviar de manera OBLIGATORIA la JWT sino sera rechazado
    def get(self):
        id=get_jwt_identity() # devolvera el identificador de la jwt, es decir, el valor contenido en jti dentro del payload
        usuarioEncontrado = db.session.query(Usuario).filter(Usuario.id==id).first()

        resultado=AuthLoginDeserializer.model_validate(usuarioEncontrado).model_dump(mode="json")
        return{
            "content": resultado
        }
