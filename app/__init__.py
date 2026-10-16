from flask import Flask
from .config import config_map
from .extensions import db, migrate
# Importamos los modelos para que SQLAlchemy registre sus tablas y relaciones
from .models import *
# Importamos flask_resful import Api
from flask_restful import Api
# Importamos controladores
from .api import ClientesController, ClienteController
#*******************************************************************************
from .api import UsuariosController, UsuarioController,SuperUsuariosController
#*******************************************************************************
from .api import ClientesUsuariosController
from .api import CredencialesLocalesController
from .api import AuthLoginController,UserController
from .api import PaisesController
from uuid import UUID
from flask_jwt_extended import JWTManager

# Al usar el patron de diseño Application Factory se recomienda crear una funcion llamada create_app en la cual se inicializara todo el proyecto y asi mismo puede recibir parametros para los diferentes entornos de prueba


def create_app(env="development"):
    app = Flask(__name__)
    # Creamos la instancia de Api
    api = Api(app)
    # Aca inicializamos la instancia de JWT para que pueda ser utilizada en todo el proyecto
    JWTManager(app)
    # from_object > actualiza los valores que le pasemos en el parametro para que la instancia de Flask arranque con esas modificaciones de sus parametros, por ejemplo Debug, entre otros
    app.config.from_object(config_map[env])

    # Inicializamos la instancia de la base de datos pasandole la instancia de Flask para que utilice las variables que hemos configurado en la instancia (config_map)
    db.init_app(app)

    # Inicializamos la instancia de las migraciones para ahora declara nuestra configuracion de la instancia de flask y nuestra configuracion de la base de datos
    migrate.init_app(app, db)

    # Registramos las rutas de nuestra Api
    # add_resource(Controlador,"Ruta/Endpoint")
    api.add_resource(ClientesController, "/clientes")

    api.add_resource(UsuariosController, "/usuarios")
    api.add_resource(UsuarioController, "/usuario/<uuid:id>")
    api.add_resource(ClientesUsuariosController, "/clientes-usuarios")
    api.add_resource(CredencialesLocalesController, "/credenciales-locales")
    api.add_resource(AuthLoginController, "/auth/login")
    api.add_resource(UserController, "/auth/me")
    #***************************************************************
    api.add_resource(SuperUsuariosController, "/super-usuarios")
    #***************************************************************
    api.add_resource(PaisesController,"/paises")
    # Al momento de registrar una ruta y si esta contiene <> significara que esta parte de la rutoa es dimamica, es decir, aceptara valores y los pondra en esa variable, y esta variable tiene que tener el mismo nombre al momento de definir el meto, se puede restringir el tipo de dato poniendo antes el tipo y luego:
    api.add_resource(ClienteController, "/cliente/<uuid:id>")
    
    return app
