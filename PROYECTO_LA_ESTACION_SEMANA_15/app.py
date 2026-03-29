from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Conexion.conexion import obtener_conexion
from models.usuario import Usuario
from services.producto_service import ProductoService
from services.reporte_service import ReporteService

app = Flask(__name__)
app.secret_key = 'la_estacion_2026_secreto'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        user_data = cursor.fetchone()
        db.close()
        if user_data:
            return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
    return None

# RUTA DE PANEL (Para solucionar el BuildError de tus capturas)
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", 
                       (request.form['email'], request.form['password']))
        user = cursor.fetchone()
        db.close()
        if user:
            login_user(Usuario(user['id_usuario'], user['nombre'], user['email'], user['password']))
            return redirect(url_for('listar_productos'))
        flash("Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/productos')
@login_required
def listar_productos():
    productos = ProductoService.listar_todos()
    return render_template('productos/listado.html', productos=productos)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        try:
            # Capturamos los datos del formulario
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = request.form.get('precio')
            stock = request.form.get('stock')
            
            ProductoService.crear(nombre, descripcion, precio, stock)
            flash("¡Producto guardado exitosamente!")
            return redirect(url_for('listar_productos'))
        except Exception as e:
            flash(f"Error al guardar: {e}")
            
    return render_template('productos/crear.html')

@app.route('/reporte/pdf')
@login_required
def generar_reporte():
    productos = ProductoService.listar_todos()
    if not productos:
        return "No hay productos para generar el reporte. Registra uno primero."
    return ReporteService.generar_pdf_productos(productos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)