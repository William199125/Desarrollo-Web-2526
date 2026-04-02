from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Conexion.conexion import obtener_conexion
from models.usuario import Usuario
import math

app = Flask(__name__)
app.secret_key = 'la_estacion_final_2026'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s AND estado = 1", (user_id,))
        u = cursor.fetchone()
        db.close()
        if u:
            return Usuario(u['id_usuario'], u['nombre'], u['email'], u['password'])
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

# --- AUTENTICACIÓN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = obtener_conexion()
        if not db:
            flash("Error de conexión", "danger")
            return render_template('login.html')
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s AND estado = 1", 
                       (request.form.get('email'), request.form.get('password')))
        user = cursor.fetchone()
        db.close()
        if user:
            login_user(Usuario(user['id_usuario'], user['nombre'], user['email'], user['password']))
            return redirect(url_for('panel'))
        flash("Usuario o clave incorrectos", "danger")
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        try:
            email = request.form.get('email')
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("El correo ya existe", "warning")
                return redirect(url_for('registro'))
            cursor.execute("INSERT INTO usuarios (nombre, email, password, estado) VALUES (%s, %s, %s, 1)", 
                           (request.form.get('nombre'), email, request.form.get('password')))
            db.commit()
            flash("Registro exitoso", "success")
            return redirect(url_for('login'))
        except:
            flash("Error al registrar", "danger")
        finally:
            db.close()
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- DASHBOARD ---
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

@app.route('/api/dashboard')
@login_required
def api_dashboard():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as t FROM clientes WHERE estado = 1")
    c = cursor.fetchone()['t']
    cursor.execute("SELECT COUNT(*) as t FROM productos")
    p = cursor.fetchone()['t']
    cursor.execute("SELECT COUNT(*) as t FROM ventas")
    v = cursor.fetchone()['t']
    cursor.execute("SELECT COALESCE(SUM(total), 0) as i FROM ventas")
    i = cursor.fetchone()['i']
    db.close()
    return jsonify({'clientes': c, 'productos': p, 'ventas': v, 'ingresos': float(i)})

@app.route('/api/reportes/<tipo>')
@login_required
def api_reportes(tipo):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    if tipo == 'clientes':
        cursor.execute("SELECT id_cliente, nombre, cedula, telefono FROM clientes WHERE estado = 1")
    elif tipo == 'productos':
        cursor.execute("SELECT id_producto, nombre, categoria, stock, precio FROM productos")
    elif tipo == 'ventas':
        cursor.execute("""
            SELECT v.id_venta, c.nombre as cliente, p.nombre as producto, v.cantidad, v.total, DATE_FORMAT(v.fecha, '%Y-%m-%d') as fecha
            FROM ventas v JOIN clientes c ON v.id_cliente = c.id_cliente JOIN productos p ON v.id_producto = p.id_producto
        """)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)

# --- MÓDULO PRODUCTOS ---
@app.route('/productos')
@login_required
def listar_productos():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    search = request.args.get('q', '')
    if search:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    db.close()
    return render_template('productos/listado.html', productos=productos, search=search)

@app.route('/productos/nuevo', methods=['POST'])
@login_required
def crear_producto():
    db = obtener_conexion()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES (%s, %s, %s, %s, %s)",
                       (request.form.get('nombre'), request.form.get('descripcion'), request.form.get('precio'), request.form.get('stock'), request.form.get('categoria')))
        db.commit()
        flash("Producto guardado", "success")
    finally:
        db.close()
    return redirect(url_for('listar_productos'))

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria=%s WHERE id_producto=%s",
                       (request.form.get('nombre'), request.form.get('descripcion'), request.form.get('precio'), request.form.get('stock'), request.form.get('categoria'), id))
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
    try:
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
        db.commit()
    except:
        flash("No se puede eliminar: tiene ventas asociadas", "danger")
    db.close()
    return redirect(url_for('listar_productos'))

# --- MÓDULO CLIENTES ---
@app.route('/clientes')
@login_required
def listar_clientes():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE estado = 1")
    clientes = cursor.fetchall()
    db.close()
    return render_template('clientes/listado.html', clientes=clientes)

@app.route('/clientes/nuevo', methods=['POST'])
@login_required
def crear_cliente():
    db = obtener_conexion()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO clientes (nombre, cedula, correo, telefono, estado) VALUES (%s, %s, %s, %s, 1)",
                       (request.form.get('nombre'), request.form.get('cedula'), request.form.get('correo'), request.form.get('telefono')))
        db.commit()
    finally:
        db.close()
    return redirect(url_for('listar_clientes'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("UPDATE clientes SET nombre=%s, cedula=%s, correo=%s, telefono=%s WHERE id_cliente=%s",
                       (request.form.get('nombre'), request.form.get('cedula'), request.form.get('correo'), request.form.get('telefono'), id))
        db.commit()
        db.close()
        return redirect(url_for('listar_clientes'))
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()
    db.close()
    return render_template('clientes/editar.html', cliente=cliente)

@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    db = obtener_conexion()
    cursor = db.cursor()
    cursor.execute("UPDATE clientes SET estado = 0 WHERE id_cliente = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('listar_clientes'))

# --- MÓDULO VENTAS ---
@app.route('/ventas')
@login_required
def listar_ventas():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT v.id_venta, c.nombre as cliente, p.nombre as producto, v.cantidad, v.total, v.fecha 
        FROM ventas v JOIN clientes c ON v.id_cliente = c.id_cliente JOIN productos p ON v.id_producto = p.id_producto
        ORDER BY v.fecha DESC
    """)
    ventas = cursor.fetchall()
    db.close()
    return render_template('ventas/listado.html', ventas=ventas)

@app.route('/ventas/nueva', methods=['GET', 'POST'])
@login_required
def registrar_venta():
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        id_p = request.form.get('id_producto')
        cant = int(request.form.get('cantidad'))
        cursor.execute("SELECT stock, precio FROM productos WHERE id_producto = %s", (id_p,))
        prod = cursor.fetchone()
        if prod and prod['stock'] >= cant:
            total = cant * float(prod['precio'])
            cursor.execute("INSERT INTO ventas (id_usuario, id_cliente, id_producto, cantidad, total) VALUES (%s, %s, %s, %s, %s)",
                           (current_user.id, request.form.get('id_cliente'), id_p, cant, total))
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s", (cant, id_p))
            db.commit()
            flash("Venta exitosa", "success")
            db.close()
            return redirect(url_for('listar_ventas'))
        flash("No hay stock", "danger")
        db.close()
        return redirect(url_for('registrar_venta'))
    cursor.execute("SELECT * FROM clientes WHERE estado = 1")
    cls = cursor.fetchall()
    cursor.execute("SELECT * FROM productos WHERE stock > 0")
    pds = cursor.fetchall()
    db.close()
    return render_template('ventas/nueva.html', clientes=cls, productos=pds)

@app.route('/ventas/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_venta(id):
    db = obtener_conexion()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, cantidad FROM ventas WHERE id_venta = %s", (id,))
    v = cursor.fetchone()
    if v:
        cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s", (v['cantidad'], v['id_producto']))
        cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (id,))
        db.commit()
    db.close()
    return redirect(url_for('listar_ventas'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)