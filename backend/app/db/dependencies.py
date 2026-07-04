from app.db.database import SessionLocal

# Esta función es un generador que se utiliza para obtener una sesión de base de datos.
# Se utiliza en las rutas de FastAPI para obtener una sesión de base de datos que se puede utilizar para realizar operaciones CRUD.
def get_db():
    db = SessionLocal()
    try:

        yield db

    finally:
        db.close()

# yield es para devolver la sesión de base de datos al llamador y luego continuar ejecutando el código después del yield cuando se cierra la sesión.
# El uso de yield permite que la sesión de base de datos se cierre automáticamente después de que se haya utilizado.