# CRUD FLASK PYTHON + MYSQL
# Desarrollado por: Cristian Redondo

# Importamos la librería para conectarnos a MySQL
import pymysql

# Función para obtener una conexión a la base de datos
def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='app_crud_juego'
    )