import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="201624", # Tu contraseña confirmada
            database="la_estacion_db",
            port=3308, # Tu puerto de instalación
            auth_plugin='mysql_native_password'
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None 