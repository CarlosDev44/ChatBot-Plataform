from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.config import DATABASE_URL

#Configuración de la base de datos utilizando SQLAlchemy.

#Engine es el objeto que representa la conexión a la base de datos.
engine = create_engine(DATABASE_URL)

#SessionLocal es una clase que se utiliza para crear sesiones de base de datos.
#Cada vez que se llama a SessionLocal(), se crea una nueva sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base es para la creación de modelos de base de datos.
#Todos los modelos deben heredar de esta clase porque contiene la información 
#Necesaria para que SQLAlchemy pueda mapear las clases a las tablas de la base de datos.
Base = declarative_base()