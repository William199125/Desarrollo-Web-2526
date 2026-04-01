import mysql.connector
from mysql.connector import Error
import os

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            # Si existe la variable en Render la usa, si no, usa tus datos locales
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '201624'),
            database=os.getenv('DB_NAME', 'la_estacion_db'),
            port=int(os.getenv('DB_PORT', 3308)),
            auth_plugin='mysql_native_password'
        )
        if conexion.is_connected():
            conexion.autocommit = True # Guarda los datos automáticamente
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None