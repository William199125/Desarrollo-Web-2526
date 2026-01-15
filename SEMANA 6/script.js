document.addEventListener('DOMContentLoaded', () => {
    // 1. Selección de elementos del DOM
    const form = document.getElementById('registroForm');
    const nombre = document.getElementById('nombre');
    const email = document.getElementById('email');
    const edad = document.getElementById('edad');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const btnSubmit = document.getElementById('btnSubmit');
    const btnReset = document.getElementById('btnReset');

    // Objeto para rastrear el estado de validez de cada campo
    const formValidity = {
        nombre: false,
        email: false,
        edad: false,
        password: false,
        confirmPassword: false
    };

    // 2. Funciones de Ayuda (Utilitarias)
    
    // Función para mostrar error o éxito visualmente
    const setStatus = (input, isValid, message = '') => {
        const errorSpan = document.getElementById(`error-${input.id}`);
        
        if (isValid) {
            input.classList.remove('error');
            input.classList.add('success');
            errorSpan.classList.remove('visible');
            errorSpan.textContent = '';
        } else {
            input.classList.remove('success');
            input.classList.add('error');
            errorSpan.textContent = message;
            errorSpan.classList.add('visible');
        }
    };

    // Función para habilitar/deshabilitar el botón de envío
    const validateForm = () => {
        // Verifica si todos los valores en formValidity son true
        const allValid = Object.values(formValidity).every(status => status === true);
        btnSubmit.disabled = !allValid;
    };

    // 3. Validaciones Específicas

    // Validar Nombre (Mínimo 4 caracteres)
    nombre.addEventListener('input', () => {
        const value = nombre.value.trim();
        if (value.length >= 4) {
            formValidity.nombre = true;
            setStatus(nombre, true);
        } else {
            formValidity.nombre = false;
            setStatus(nombre, false, 'El nombre debe tener al menos 4 caracteres.');
        }
        validateForm();
    });

    // Validar Correo (Regex)
    email.addEventListener('input', () => {
        // Expresión regular estándar para emails
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (regex.test(email.value.trim())) {
            formValidity.email = true;
            setStatus(email, true);
        } else {
            formValidity.email = false;
            setStatus(email, false, 'Introduce un correo electrónico válido.');
        }
        validateForm();
    });

    // Validar Edad (>= 18)
    edad.addEventListener('input', () => {
        const value = parseInt(edad.value);
        if (value >= 18) {
            formValidity.edad = true;
            setStatus(edad, true);
        } else {
            formValidity.edad = false;
            setStatus(edad, false, 'Debes ser mayor de 18 años.');
        }
        validateForm();
    });

    // Validar Contraseña (Min 10 chars, 1 numero, 1 especial)
    password.addEventListener('input', () => {
        const value = password.value;
        // Regex: Al menos un número (?=.*\d), un caracter especial (?=.*[\W_]), min 10 chars
        const regex = /^(?=.*\d)(?=.*[\W_]).{10,}$/;

        if (regex.test(value)) {
            formValidity.password = true;
            setStatus(password, true);
        } else {
            formValidity.password = false;
            setStatus(password, false, 'Mínimo 10 caracteres, un número y un símbolo.');
        }
        
        // Si cambiamos la contraseña, debemos revalidar la confirmación
        if (confirmPassword.value !== '') {
            // Disparar evento manual para re-chequear coincidencia
            confirmPassword.dispatchEvent(new Event('input'));
        }
        validateForm();
    });

    // Validar Confirmación de Contraseña
    confirmPassword.addEventListener('input', () => {
        if (confirmPassword.value === password.value && password.value !== '') {
            formValidity.confirmPassword = true;
            setStatus(confirmPassword, true);
        } else {
            formValidity.confirmPassword = false;
            setStatus(confirmPassword, false, 'Las contraseñas no coinciden.');
        }
        validateForm();
    });

    // 4. Manejo de Botones

    // Enviar formulario
    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Evita que la página se recargue
        if (!btnSubmit.disabled) {
            alert('¡Formulario enviado con éxito! Todos los datos son válidos.');
            // Aquí podrías agregar la lógica para enviar al servidor
        }
    });

    // Reiniciar formulario
    btnReset.addEventListener('click', () => {
        form.reset(); // Limpia los inputs
        
        // Limpiar clases visuales y estados
        document.querySelectorAll('input').forEach(input => {
            input.classList.remove('success', 'error');
        });
        document.querySelectorAll('.error-msg').forEach(span => {
            span.classList.remove('visible');
        });

        // Resetear objeto de validez
        Object.keys(formValidity).forEach(key => formValidity[key] = false);
        
        validateForm(); // Deshabilitará el botón nuevamente
    });
});