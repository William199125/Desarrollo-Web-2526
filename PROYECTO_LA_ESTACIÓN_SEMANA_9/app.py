from flask import Flask

app = Flask(__name__)

# RUTA PRINCIPAL (Punto 2 de la tarea)
@app.route('/')
def home():
    # Usamos tu eslogan real [cite: 86]
    return """
    <h1>La Estación de los Detalles</h1>
    <p><i>"Tu parada obligatoria para celebrar con sabor y estilo"</i></p>
    <hr>
    <h3>Nuestras Estaciones o "Vías":</h3>
    <ul>
        <li><b>Vía 1:</b> Parada Personalizada (Amigurumis y Velas) [cite: 94]</li>
        <li><b>Vía 2:</b> Parada de Eventos (Catering Gourmet) [cite: 98]</li>
        <li><b>Vía 3:</b> Parada del Sabor (Alitas y Pizzas) [cite: 101]</li>
    </ul>
    """

# RUTA DINÁMICA (Punto 3 de la tarea)
# Ejemplo: si navegas a /detalle/Amigurumi
@app.route('/detalle/<nombre>')
def ver_detalle(nombre):
    return f"<h1>Detalle: {nombre}</h1><p>En La Estación, cada {nombre} se crea con alma y creatividad.</p>"

if __name__ == '__main__':
    app.run(debug=True) 