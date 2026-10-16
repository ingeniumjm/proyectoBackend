# Ahora todos los metodos(GET, POST, PUT, DELETE) se definiran como metodos de una clase
from flask_restful import Resource, request

# importamos ClienteSerializar
from app.schemas import PaisesDeserializer,PaisesSerializer
from pydantic import ValidationError, TypeAdapter
from app.models import Pais
from app.extensions import db


class PaisesController(Resource):

    def get(self):
        # SELECT * FROM categorias;
        paises = db.session.query(Pais).all()
        # TypeAdaptar es una clase que me permite modificar el Deserializador para poder agregarle que puedo pasarle un conjunto de instancias, ya que solamente aceptara una
        adaptador_paises = TypeAdapter(list[PaisesDeserializer])
        # validate_python se usa para poder hacer la validacin de la informacion proveniente de las instancias del modelo y convertirlas a instancias del Desesializador
        resultado = adaptador_paises.validate_python(paises)
        print(resultado)
        return {
            "message": "Los paises son:",
            # dump_python convertimos el lconjuto de instancias del deserializador a un formato que pueda ser devuelto, es decir, en este caso usaremos un formato json
            "content": adaptador_paises.dump_python(resultado, mode='json')

        }  # su codigo de estado por defecto es 200

    def post(self):
        data = request.get_json()
        # Siempre hay que validar la data antes de mandarla a la bd
        # Si al momento de validad la informacion falla, emitira un error de tipo ValidationError
        try:
            informacionSerializada = PaisesSerializer.model_validate(
                data)
            print(informacionSerializada)

            # Ahora que sabemos que la info es correcta, lprocedemos con el guardado en la base de datos

            # INSERT INT0 clientes (razon_social) VALUES (...);
            # un dict que luego se convierte en objeto(se expande)
            nuevoPais = Pais(**informacionSerializada.model_dump())

            # Aca agregamos el nuevo registro a la bd
            db.session.add(nuevoPais)

            # Aca agregamos el registro de manera permanente
            db.session.commit()

            return {
                "message": "Pais creada exitosamente"
            }, 201  # Created
        except ValidationError as error:
            return {
                "message": "Error al crear pais",
                "content": error.errors()
            }, 405  # bad request

