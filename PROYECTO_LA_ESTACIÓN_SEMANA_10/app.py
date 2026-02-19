from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Renderizamos la plantilla index.html en lugar de devolver texto plano
    return render_template('index.html')

# Agrega una ruta extra como pidió el ingeniero (ejemplo: productos)
@app.route('/productos')
def productos():
    return render_template('index.html') # Luego puedes crear productos.html

if __name__ == '__main__':
    app.run(debug=True) 