from Conexion.conexion import obtener_conexion
from models.producto import Producto

class ProductoService:
    @staticmethod
    def listar_todos():
        db = obtener_conexion()
        if not db: return []
        cursor = db.cursor(dictionary=True)
        # Traemos todo de la tabla productos
        cursor.execute("SELECT * FROM productos")
        datos = cursor.fetchall()
        db.close()
        return [Producto(**d) for d in datos]

    @staticmethod
    def crear(nombre, descripcion, precio, stock):
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            # IMPORTANTE: Verifica que estas columnas existan en tu MySQL Workbench
            sql = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio, stock))
            # No hace falta commit() si usas autocommit en conexion.py
            db.close()