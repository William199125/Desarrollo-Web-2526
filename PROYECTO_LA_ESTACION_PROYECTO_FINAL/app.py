from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Conexion.conexion import obtener_conexion
from models.usuario import Usuario
from services.producto_service import ProductoService
from services.reporte_service import ReporteService

app = Flask(__name__)
app.secret_key = 'la_estacion_pro_2026'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        u = cursor.fetchone()
        db.close()
        if u:
            return Usuario(u['id_usuario'], u['nombre'], u['email'], u['password'])
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", 
                       (request.form.get('email'), request.form.get('password')))
        user = cursor.fetchone()
        db.close()
        if user:
            login_user(Usuario(user['id_usuario'], user['nombre'], user['email'], user['password']))
            return redirect(url_for('panel'))
        flash("Credenciales incorrectas")
    return render_template('login.html')

@app.route('/panel')
@login_required
def panel():
    db = obtener_conexion()
    labels, values = [], []
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT nombre, stock FROM productos ORDER BY stock ASC LIMIT 5")
        datos = cursor.fetchall()
        db.close()
        labels = [p['nombre'] for p in datos]
        values = [p['stock'] for p in datos]
    return render_template('panel.html', labels=labels, values=values)

# --- INICIO DEL CRUD DE PRODUCTOS ---
@app.route('/productos')
@login_required
def listar_productos():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    db.close()
    return render_template('productos/listado.html', productos=productos)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
                       (request.form.get('nombre'), request.form.get('descripcion'), request.form.get('precio'), request.form.get('stock')))
        db.commit()
        db.close()
        return redirect(url_for('listar_productos'))
    return render_template('productos/crear.html')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id_producto=%s",
                       (request.form.get('nombre'), request.form.get('descripcion'), request.form.get('precio'), request.form.get('stock'), id))
        db.commit()
        db.close()
        return redirect(url_for('listar_productos'))
    
    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
    producto = cursor.fetchone()
    db.close()
    return render_template('productos/editar.html', producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    db = obtener_conexion()
    cursor = db.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('listar_productos'))
# --- FIN DEL CRUD ---

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def registro_usuario():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                       (request.form.get('nombre'), request.form.get('email'), request.form.get('password')))
        db.commit()
        db.close()
        return redirect(url_for('panel'))
    return render_template('registro_usuario.html')

@app.route('/reporte/pdf')
@login_required
def generar_reporte():
    productos = ProductoService.listar_todos()
    return ReporteService.generar_pdf_productos(productos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)