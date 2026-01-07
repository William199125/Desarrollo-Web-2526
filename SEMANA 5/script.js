// Selección de elementos
const input = document.getElementById('imageInput');
const addBtn = document.getElementById('addBtn');
const deleteBtn = document.getElementById('deleteBtn');
const gallery = document.getElementById('gallery');

// Función Agregar
addBtn.addEventListener('click', () => {
    const url = input.value;
    if (url === '') {
        alert('Por favor escribe una URL');
        return;
    }

    const img = document.createElement('img');
    img.src = url;
    img.className = 'gallery-img';

    // Evento Click en la imagen nueva
    img.addEventListener('click', () => {
        // Quitar selección a la anterior
        const anterior = document.querySelector('.selected');
        if (anterior) {
            anterior.classList.remove('selected');
        }
        
        // Seleccionar la nueva
        img.classList.add('selected');
        deleteBtn.disabled = false; // Activar botón borrar
    });

    gallery.appendChild(img);
    input.value = ''; // Limpiar input
});

// Función Borrar
deleteBtn.addEventListener('click', () => {
    const seleccionada = document.querySelector('.selected');
    if (seleccionada) {
        seleccionada.remove();
        deleteBtn.disabled = true;
    }
});

// Atajos de teclado (Bonus)
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addBtn.click();
    if (e.key === 'Delete' || e.key === 'Backspace') deleteBtn.click();
});