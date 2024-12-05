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



#Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    mydb = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="",
        database = "app_crud_juego"
        )
    return mydb
    '''       
    if mydb:
        return ("Conexion exitosa")
    else:
        return ("Error en la conexion a BD")
    '''
    
    