from flask import Flask, render_template, request, redirect, url_for
from inventario import Inventario, Producto # Importamos nuestras clases

app = Flask(__name__)
# Instanciamos el inventario (esto conecta con la DB automáticamente)
sistema_inventario = Inventario()

@app.route('/')
def index():
    # Obtiene todos los productos de la base de datos usando nuestra clase
    productos = sistema_inventario.obtener_todos()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    # Recibimos los datos del formulario
    id_p = request.form.get('id')
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    
    # Creamos el objeto Producto y lo guardamos
    nuevo_prod = Producto(id_p, nombre, cantidad, precio)
    sistema_inventario.agregar_producto(nuevo_prod)
    
    return redirect(url_for('index'))

@app.route('/eliminar/<id_p>')
def eliminar(id_p):
    sistema_inventario.eliminar_producto(id_p)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 