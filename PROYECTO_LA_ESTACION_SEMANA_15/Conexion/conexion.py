import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="201624",
            database="la_estacion_db",
            port=3308,
            auth_plugin='mysql_native_password'
        )
        if conexion.is_connected():
            conexion.autocommit = True # Guarda los datos automáticamente
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None