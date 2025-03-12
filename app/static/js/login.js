document.addEventListener('DOMContentLoaded', function() {
    // Función para mostrar/ocultar contraseña
    const togglePassword = document.querySelector('#togglePassword');
    const passwordField = document.querySelector('#password');
    
    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            // Cambiar el tipo de input
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            
            // Cambiar el icono
            togglePassword.classList.toggle('fa-eye');
            togglePassword.classList.toggle('fa-eye-slash');
        });
    }
});