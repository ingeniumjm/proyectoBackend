from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Aca inicializamos el uso del ORM
db=SQLAlchemy()

#Aca inicilizamos el uso del administrado de migracions de la bd
migrate=Migrate()
