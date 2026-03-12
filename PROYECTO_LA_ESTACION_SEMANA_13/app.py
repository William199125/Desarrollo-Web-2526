from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.conexion import obtener_conexion 

app = Flask(__name__)
app.secret_key = 'estacion_201624'

@app.route('/')
def index():
    return render_template('index.html')

# Mostrar usuarios (Punto 4 de la tarea)
@app.route('/usuarios')
def lista_usuarios():
    db = obtener_conexion()
    if db:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        datos = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('usuarios.html', usuarios=datos)
    return "Error de conexión con la base de datos."

# Agregar usuario (Ruta corregida para evitar 404)
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form['nombre']
    mail = request.form['mail']
    password = request.form['password']
    
    db = obtener_conexion()
    if db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nombre, mail, password))
        db.commit()
        cursor.close()
        db.close()
        flash('Registro exitoso')
    return redirect(url_for('lista_usuarios'))

# Eliminar usuario
@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    db = obtener_conexion()
    if db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        db.commit()
        db.close()
    return redirect(url_for('lista_usuarios'))

if __name__ == '__main__':
    app.run(debug=True)