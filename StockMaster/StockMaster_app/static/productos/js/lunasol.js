// Código JavaScript para guardar el tema actual del usuario en el almacenamiento web
let currentTheme = localStorage.getItem('theme') || 'light';

// Elementos de icono del sol y la luna
const sunIcon = document.getElementById("sunIcon");
const moonIcon = document.getElementById("moonIcon");

// Función para cambiar el tema
function toggleTheme() {
    if (currentTheme === "dark") {
        // Cambia al tema claro
        document.body.classList.remove('dark-theme-variables');
        sunIcon.style.transform = "scale(1)";
        moonIcon.style.transform = "scale(0)";
        currentTheme = 'light';
    } else {
        // Cambia al tema oscuro
        document.body.classList.add('dark-theme-variables');
        sunIcon.style.transform = "scale(0)";
        moonIcon.style.transform = "scale(1)";
        currentTheme = 'dark';
    }
    localStorage.setItem('theme', currentTheme);
}

// Agrega un evento de clic al botón de cambio de tema
const themeToggleBtn = document.getElementById("themeToggleBtn");
themeToggleBtn.addEventListener("click", toggleTheme);

// Aplica el tema inicial
if (currentTheme === "dark") {
    document.body.classList.add('dark-theme-variables');
    sunIcon.style.transform = "scale(0)";
    moonIcon.style.transform = "scale(1)";
}
