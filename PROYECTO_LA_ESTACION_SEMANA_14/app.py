from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from Conexion.conexion import obtener_conexion
from models import Usuario

app = Flask(__name__)
app.secret_key = 'clave_secreta_estacion_2026'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
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

# Evita el error 404 redirigiendo al login
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        db = obtener_conexion()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                               (nombre, email, password))
                db.commit()
                flash('¡Registro exitoso! Ya puedes iniciar sesión.')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f'Error en registro: {e}')
            finally:
                db.close()
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_form = request.form['email']
        pass_form = request.form['password']
        db = obtener_conexion()
        if db:
            cursor = db.cursor(dictionary=True)
            # Buscamos por 'email' como pide la tarea
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email_form, pass_form))
            user_data = cursor.fetchone()
            db.close()
            if user_data:
                user_obj = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
                login_user(user_obj)
                return redirect(url_for('panel'))
            else:
                flash('Correo o contraseña incorrectos.')
    return render_template('login.html')

@app.route('/panel')
@login_required # Ruta protegida
def panel():
    return render_template('panel.html', usuario=current_user.nombre)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)