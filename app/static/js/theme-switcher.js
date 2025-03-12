document.addEventListener('DOMContentLoaded', function() {
    // Obtener el tema del localStorage o usar 'light' como predeterminado
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Aplicar el tema guardado
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    // Actualizar el texto e icono del botón según el tema
    updateToggleButton(currentTheme);
    
    // Agregar evento de clic al botón de cambio de tema
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            // Obtener el tema actual
            const currentTheme = document.documentElement.getAttribute('data-theme');
            
            // Cambiar al tema opuesto
            const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
            
            // Actualizar el atributo data-theme
            document.documentElement.setAttribute('data-theme', newTheme);
            
            // Guardar el tema en localStorage
            localStorage.setItem('theme', newTheme);
            
            // Actualizar el texto e icono del botón
            updateToggleButton(newTheme);
        });
    }
});

// Función para actualizar el botón según el tema
function updateToggleButton(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        if (theme === 'dark') {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i> Modo Claro';
            themeToggle.classList.remove('btn-light');
            themeToggle.classList.add('btn-dark');
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i> Modo Oscuro';
            themeToggle.classList.remove('btn-dark');
            themeToggle.classList.add('btn-light');
        }
    }
}