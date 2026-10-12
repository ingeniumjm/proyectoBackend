from flask_restful import Resource, request
from app.models import Usuario
from app.extensions import db
from app.schemas import UsuarioSerializer, UsuarioDeserializer
from pydantic import ValidationError, TypeAdapter
from sqlalchemy.exc import IntegrityError


class UsuariosController(Resource):
    def post(self):
        data = request.get_json()
        try:
            dataValidada = UsuarioSerializer.model_validate(data)

            nuevoUsuario = Usuario(**dataValidada.model_dump())
            db.session.add(nuevoUsuario)
            db.session.commit()

            return {
                "message": "Usuario creado exitosamente"
            }, 201

        except ValidationError as error:
            return {
                'message': 'Error al crear usuario',
                'content': error.errors()
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {
                "message": "Ya existe un usuario registrado con ese correo electronico"
            }

    def get(self):
        usuarios = db.session.query(Usuario).filter(
            Usuario.estado != "inactivo").all()
        adaptador = TypeAdapter(list[UsuarioDeserializer])
        informacion = adaptador.validate_python(usuarios)

        return {
            'content': adaptador.dump_python(informacion, mode='json')
        }


class UsuarioController(Resource):
    def delete(self, id):
        # Soft delete (eliminacion suave) porque no se elem,ina el registro como tal len la bd, si no que solo cambia su estado(col inactivo)

        # SELECT id FROM usuarios
        usuarioEncontrado = db.session.query(Usuario).with_entities(
            Usuario.id).filter(Usuario.id == id, Usuario.estado == "inactivo").first()
        if not usuarioEncontrado:
            return {
                "message": "Usuario no existe"
            }, 404
        # Tambien se puede realizar la actualizacoin mediante el metodo update
        db.session.query(Usuario).filter(
            Usuario.id == id).update({Usuario.estado: "inactivo"})
        db.session.commit()
        return {
            "message": "Usuario eliminado exitosamente"
        }
