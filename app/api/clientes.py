# Ahora todos los metodos(GET, POST, PUT, DELETE) se definiran como metodos de una clase
from flask_restful import Resource, request

# importamos ClienteSerializar
from app.schemas import ClienteSerializer, ClienteDeserializer
from pydantic import ValidationError, TypeAdapter
from app.models import Cliente
from app.extensions import db


class ClientesController(Resource):

    def get(self):
        # SELECT * FROM categorias;
        clientes = db.session.query(Cliente).all()
        print(clientes)
        # TypeAdaptar es una clase que me permite modificar el Deserializador para poder agregarle que puedo pasarle un conjunto de instancias, ya que solamente aceptara una
        adaptador_clientes = TypeAdapter(list[ClienteDeserializer])
        # validate_python se usa para poder hacer la validacin de la informacion proveniente de las instancias del modelo y convertirlas a instancias del Desesializador
        resultado = adaptador_clientes.validate_python(clientes)
        print(resultado)
        return {
            "message": "Los clientes son:",
            # dump_python convertimos el lconjuto de instancias del deserializador a un formato que pueda ser devuelto, es decir, en este caso usaremos un formato json
            "content": adaptador_clientes.dump_python(resultado, mode='json')

        }  # su codigo de estado por defecto es 200

    def post(self):
        data = request.get_json()
        # Siempre hay que validar la data antes de mandarla a la bd
        # Si al momento de validad la informacion falla, emitira un error de tipo ValidationError
        try:
            informacionSerializada = ClienteSerializer.model_validate(
                data)
            print(informacionSerializada)

            # Ahora que sabemos que la info es correcta, lprocedemos con el guardado en la base de datos

            # INSERT INT0 clientes (razon_social) VALUES (...);
            # un dict que luego se convierte en objeto(se expande)
            nuevoCliente = Cliente(**informacionSerializada.model_dump())

            # Aca agregamos el nuevo registro a la bd
            db.session.add(nuevoCliente)

            # Aca agregamos el registro de manera permanente
            db.session.commit()

            return {
                "message": "Cliente creada exitosamente"
            }, 201  # Created
        except ValidationError as error:
            return {
                "message": "Error al crear cliente",
                "content": error.errors()
            }, 405  # bad request


class ClienteController(Resource):
    # Este sera la encargada de la gestion de una sola categoria (segun su id)
    def validarCliente(self,id):
        # el filter se usa en comparacion > filter(Cliente.id==1)
        # el filter_by se usa en asignacion > filter_by(id=1)
        # SELECT * FROM clientes WHERE id= ... LIMIT 1;
        clienteEncontrado = db.session.query(
            Cliente).filter(Cliente.id == id).first()
        return clienteEncontrado


    def get(self, id):
        clienteEncontrado =self.validarCliente(id)
        if not clienteEncontrado:
            return {
                'message': 'Cliente no existe'
            }, 404

        respuesta = ClienteDeserializer.model_validate(
            clienteEncontrado).model_dump(mode='json')

        return {
            'content': respuesta
        }

    def put(self,id):
        clienteEncontrado =self.validarCliente(id)
        if not clienteEncontrado:
            return {
                'message': 'Cliente no existe'
            }, 404    

        clienteValidado = ClienteSerializer.model_validate(request.get_json())
        # En la instancia que tengo de mi clienteEncontrado puedo modificar la informacion
        for campo, valor in clienteValidado.model_dump(exclude_unset=True).items():
            setattr(clienteEncontrado, campo, valor)

        db.session.commit()

        #Ahora obtenemos la informacion actualizada desde la categoriaEncontrada para devolberla al cliente
        resultado =ClienteDeserializer.model_validate(clienteEncontrado).model_dump(mode='json')
        return{
            'message': 'Cliente modificado exitosamente',
            'content': resultado

        }
    
    def delete (self, id):
        clienteEncontrado= self.validarCliente(id)   
        if not clienteEncontrado:
            return{
                "message":"Cliente no existe"
            }, 404
        # DELETE FROM clientes WHERE id =...;
        db.session.delete(clienteEncontrado)
        db.session.commit()
        # En los deletes permanentes se suele no retornar y solo retonar un estado 204 (No Content)
        return None,204