import sqlite3

# ==========================================
# CLASE PRODUCTO (Encapsulamiento)
# ==========================================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Atributos privados para aplicar encapsulamiento
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Métodos Getter (Obtener)
    def get_id(self): return self.__id_producto
    def get_nombre(self): return self.__nombre
    def get_cantidad(self): return self.__cantidad
    def get_precio(self): return self.__precio

    # Métodos Setter (Establecer/Modificar)
    def set_cantidad(self, nueva_cantidad): self.__cantidad = nueva_cantidad
    def set_precio(self, nuevo_precio): self.__precio = nuevo_precio
    def set_nombre(self, nuevo_nombre): self.__nombre = nuevo_nombre

    # Método para representar el objeto como diccionario (Tupla de exportación)
    def to_dict(self):
        return {
            "id": self.__id_producto,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }

# ==========================================
# CLASE INVENTARIO (Colecciones + SQLite)
# ==========================================
class Inventario:
    def __init__(self):
        # USO DE COLECCIÓN: Diccionario para búsqueda rápida por ID en memoria O(1)
        self.productos = {}
        self.db_name = 'la_estacion.db'
        self.crear_tabla()
        self.cargar_desde_db()

    def conectar(self):
        """Crea y retorna la conexión a SQLite"""
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        """Crea la tabla si no existe en la base de datos"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()

    def cargar_desde_db(self):
        """Lee la DB y llena el diccionario (Colección)"""
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall() # fetchall retorna una LISTA de TUPLAS
        
        for fila in filas:
            # Reconstruimos los objetos Producto en memoria
            producto = Producto(fila[0], fila[1], fila[2], fila[3])
            self.productos[producto.get_id()] = producto
        
        conexion.close()

    # --- OPERACIONES CRUD ---

    def agregar_producto(self, producto):
        """Añade a la DB y al diccionario"""
        if producto.get_id() in self.productos:
            return False # El producto ya existe
        
        try:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                           (producto.get_id(), producto.get_nombre(), producto.get_cantidad(), producto.get_precio()))
            conexion.commit()
            conexion.close()
            
            # Actualizamos la colección en memoria
            self.productos[producto.get_id()] = producto
            return True
        except sqlite3.IntegrityError:
            return False

    def obtener_todos(self):
        """Retorna una LISTA con todos los productos para mostrar en el HTML"""
        return [p.to_dict() for p in self.productos.values()]

    def eliminar_producto(self, id_producto):
        """Elimina de la DB y del diccionario"""
        if id_producto in self.productos:
            conexion = self.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()
            conexion.close()
            
            del self.productos[id_producto] # Eliminamos de la colección
            return True
        return False 