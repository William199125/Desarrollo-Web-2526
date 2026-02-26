from flask import Flask

app = Flask(__name__)

# RUTA PRINCIPAL: Nombre y Propósito (Punto 2)
@app.route('/')
def home():
    return """
    <h1>La Estación de los Detalles</h1>
    <p><b>Propósito:</b> Brindar experiencias memorables mediante detalles artesanales y gastronomía de alta calidad.</p>
    <p><i>"Tu parada obligatoria para celebrar con sabor y estilo"</i></p>
    <hr>
    <h3>Nuestras Vías:</h3>
    <ul>
        <li>Vía 1: Parada Personalizada (Amigurumis)</li>
        <li>Vía 2: Parada de Eventos (Catering)</li>
        <li>Vía 3: Parada del Sabor (Alitas y Pizzas)</li>
    </ul>
    """

# RUTA DINÁMICA: (Punto 3)
@app.route('/detalle/<nombre>')
def ver_detalle(nombre):
    return f"<h1>Producto: {nombre}</h1><p>En La Estación, creamos cada {nombre} con alma y creatividad artesanal.</p><a href='/'>Regresar</a>"

if __name__ == '__main__':
    app.run(debug=True) 