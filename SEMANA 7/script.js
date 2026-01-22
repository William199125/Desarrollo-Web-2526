// 1. Datos Iniciales: Arreglo de objetos (Simulando una base de datos)
const productos = [
    { nombre: "Laptop Gamer", precio: 1200, descripcion: "Alta potencia, rendimiento y no se recalienta." },
    { nombre: "Mouse Inalámbrico", precio: 25, descripcion: "Ergonómico para tu mano y batería duradera." },
    { nombre: "Teclado Inalambrico", precio: 120, descripcion: "Luces RGB y switches azules o verdes." }
];

// 2. Selección de elementos del DOM (HTML)
// Seleccionamos la lista <ul> y el botón por sus ID
const listaContainer = document.getElementById('lista-productos');
const btnAgregar = document.getElementById('btn-agregar');

// 3. Función para renderizar (dibujar) la lista
function renderizarProductos() {
    // Limpiamos la lista actual para evitar duplicados al volver a pintar
    listaContainer.innerHTML = '';

    // Recorremos el arreglo de productos
    productos.forEach(producto => {
        // Creamos un elemento <li>
        const li = document.createElement('li');

        // --- USO DE PLANTILLA (TEMPLATE LITERAL) ---
        // Usamos comillas invertidas (backticks) ` ` para mezclar HTML y variables
        li.innerHTML = `
            <h3>${producto.nombre}</h3>
            <p><strong>Precio:</strong> $${producto.precio}</p>
            <p><em>${producto.descripcion}</em></p>
        `;

        // Agregamos el <li> creado al <ul> principal
        listaContainer.appendChild(li);
    });
}

// 4. Función para agregar un producto nuevo
function agregarProducto() {
    // Creamos un producto genérico (como pide la tarea simplificada)
    // En un futuro podrías sacar estos datos de un formulario
    const nuevoProducto = {
        nombre: "Producto Nuevo " + (productos.length + 1),
        precio: Math.floor(Math.random() * 100) + 10, // Precio aleatorio entre 10 y 100
        descripcion: "Descripción generada automáticamente."
    };

    // Agregamos al arreglo de datos
    productos.push(nuevoProducto);

    // Volvemos a renderizar la lista para mostrar el cambio
    renderizarProductos();
}

// 5. Eventos
// Cuando la página carga por primera vez, mostramos los productos
document.addEventListener('DOMContentLoaded', renderizarProductos);

// Cuando hacemos clic en el botón, ejecutamos la función agregarProducto
btnAgregar.addEventListener('click', agregarProducto); 