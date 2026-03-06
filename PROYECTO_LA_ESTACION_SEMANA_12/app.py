from flask import Flask, render_template
from inventario.bd import db
from inventario.productos import Producto
# Importamos las funciones desde la carpeta 'inventario'
from inventario.inventario import guardar_txt, guardar_json, guardar_csv, leer_json

# 1. Configuración de la aplicación
app = Flask(__name__)

# Configuración de SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///la_estacion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Inicialización de BD
db.init_app(app)
with app.app_context():
    db.create_all()

# 3. Rutas
@app.route('/')
def index():
    return "Bienvenido a 'La Estación de los Detalles'. Sistema en línea."

@app.route('/agregar_test')
def agregar_test():
    # Creamos un producto de prueba
    nuevo_prod = Producto("Arreglo Floral Premium", 5, 45.50)
    
    # Guardamos en Base de Datos
    db.session.add(nuevo_prod)
    db.session.commit()
    
    # Guardamos en archivos (Persistencia adicional)
    guardar_txt(nuevo_prod)
    guardar_json(nuevo_prod)
    guardar_csv(nuevo_prod)
    
    return "Producto guardado en BD, TXT, JSON y CSV con éxito."

@app.route('/ver_inventario')
def ver_inventario():
    # Leemos desde la base de datos (SQLite)
    productos = Producto.query.all()
    return render_template('datos.html', productos=productos)

@app.route('/ver_archivos')
def ver_archivos():
    # Leemos desde el archivo JSON para cumplir con la rúbrica
    productos = leer_json()
    return render_template('datos.html', productos=productos)

# 4. Ejecución
if __name__ == '__main__':
    app.run(debug=True) 