// Esperamos a que el documento cargue completamente
document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. FUNCIONALIDAD BOTÓN DE ALERTA ---
    const botonAlerta = document.getElementById('btnAlerta');
    
    botonAlerta.addEventListener('click', function() {
        alert('¡Hola William! Has integrado JavaScript con Bootstrap correctamente.');
    });


    // --- 2. VALIDACIÓN DEL FORMULARIO ---
    const form = document.getElementById('contactForm');
    const mensajeExito = document.getElementById('mensajeExito');

    form.addEventListener('submit', function(event) {
        // Detener el envío automático para validar primero
        event.preventDefault();
        event.stopPropagation();

        let esValido = true;

        // Obtener los valores
        const nombre = document.getElementById('nombre');
        const email = document.getElementById('email');
        const mensaje = document.getElementById('mensaje');

        // Validación Nombre
        if (nombre.value.trim() === "") {
            nombre.classList.add('is-invalid'); // Clase de error de Bootstrap
            esValido = false;
        } else {
            nombre.classList.remove('is-invalid');
            nombre.classList.add('is-valid'); // Clase de éxito de Bootstrap
        }

        // Validación Email (simple: que no esté vacío y tenga @)
        if (email.value.trim() === "" || !email.value.includes('@')) {
            email.classList.add('is-invalid');
            esValido = false;
        } else {
            email.classList.remove('is-invalid');
            email.classList.add('is-valid');
        }

        // Validación Mensaje
        if (mensaje.value.trim() === "") {
            mensaje.classList.add('is-invalid');
            esValido = false;
        } else {
            mensaje.classList.remove('is-invalid');
            mensaje.classList.add('is-valid');
        }

        // Si todo es válido
        if (esValido) {
            // Mostrar mensaje de éxito
            mensajeExito.classList.remove('d-none');
            
            // Opcional: Limpiar el formulario
            form.reset();
            
            // Quitar las clases de validación visual después de unos segundos
            setTimeout(() => {
                nombre.classList.remove('is-valid');
                email.classList.remove('is-valid');
                mensaje.classList.remove('is-valid');
                mensajeExito.classList.add('d-none');
            }, 5000);
        }
    });
}); 