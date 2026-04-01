import os
import json
import csv

# Configuración de la ruta a la carpeta 'data'
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- Lógica de Escritura ---
def guardar_txt(producto):
    ruta = os.path.join(DATA_DIR, 'datos.txt')
    with open(ruta, 'a') as f:
        f.write(f"Nombre: {producto.nombre}, Cantidad: {producto.cantidad}, Precio: {producto.precio}\n")

def guardar_json(producto):
    ruta = os.path.join(DATA_DIR, 'datos.json')
    datos = []
    if os.path.exists(ruta):
        with open(ruta, 'r') as f:
            try:
                datos = json.load(f)
            except json.JSONDecodeError:
                datos = []
    
    datos.append(producto.to_dict())
    with open(ruta, 'w') as f:
        json.dump(datos, f, indent=4)

def guardar_csv(producto):
    ruta = os.path.join(DATA_DIR, 'datos.csv')
    file_exists = os.path.exists(ruta)
    with open(ruta, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Nombre', 'Cantidad', 'Precio'])
        writer.writerow([producto.nombre, producto.cantidad, producto.precio])

# --- Lógica de Lectura (para mostrar en HTML) ---
def leer_json():
    ruta = os.path.join(DATA_DIR, 'datos.json')
    if os.path.exists(ruta):
        with open(ruta, 'r') as f:
            return json.load(f)
    return [] 