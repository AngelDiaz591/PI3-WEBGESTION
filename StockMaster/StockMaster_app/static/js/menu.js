// <---------------------------------------------------Elementos--------------------------------------------------->
// Elementos para los botones de cerrar menu
const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

// Elementos de icono del sol y la luna
const sunIcon = document.getElementById("sunIcon");
const moonIcon = document.getElementById("moonIcon");

// Agrega un evento de clic al botón de cambio de tema
const themeToggleBtn = document.getElementById("themeToggleBtn");
themeToggleBtn.addEventListener("click", toggleTheme);

// Obtener la ubicación de la página actual
const currentPage = window.location.pathname;

// Obtener todos los enlaces del menú
const menuLinks = document.querySelectorAll("aside .sidebar a");

// <---------------------------------------------------Fin Elementos--------------------------------------------------->

// <------------------------------------------------Inicio de las funciones en opciones de menu------------------------------------------->
// <----------------------------------para la identificacion de la opcion del menu, en la que se encuentra------------------------------------------------>

menuLinks.forEach((link) => { // Recorrer los enlaces y comparar con la URL actual
  const linkHref = link.getAttribute("href");

  if (linkHref === currentPage) {
      link.classList.add("active"); // Agrega la clase "active" al enlace actual
  } else {
      link.classList.remove("active"); // Quita la clase "active" de otros enlaces
  }
});
// <------------------------------------------------Fin de las funciones------------------------------------------------>
// <-----------------------------Inicio de las funciones para los botones de cerrar el menú---------------------------->
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})
// <------------------------------------------------Fin de las funciones------------------------------------------------>
// <------------------------------------Inicio de las funciones para cambio de color------------------------------------>
// Código JavaScript para guardar el tema actual del usuario en el almacenamiento web
let currentTheme = localStorage.getItem('theme') || 'light';

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

// Aplica el tema inicial
if (currentTheme === "dark") {
    document.body.classList.add('dark-theme-variables');
    sunIcon.style.transform = "scale(0)";
    moonIcon.style.transform = "scale(1)";
}
// <--------------------------------------Fin de funciones para cambiar el tema-------------------------------------->
// <---------------------------------------Inicio de Guardar el dato del tema---------------------------------------->
function applyDarkTheme() {
    document.body.classList.add('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.add('active');
    themeToggler.querySelector('span:nth-child(2)').classList.remove('active');
  }
// Función para aplicar el tema claro
function applyLightTheme() {
  document.body.classList.remove('dark-theme-variables');
  themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
  themeToggler.querySelector('span:nth-child(2)').classList.add('active');
}
// Recuperar el estado del tema desde el almacenamiento web
const savedTheme = localStorage.getItem('theme');
// Verificar el tema guardado
if (savedTheme === 'dark') {
  applyDarkTheme();
} else {
  applyLightTheme();
}
// Agregar un manejador de eventos para el botón de cambio de tema
themeToggler.addEventListener('click', () => {
  if (document.body.classList.contains('dark-theme-variables')) {
    // Cambiar al tema claro
    localStorage.setItem('theme', 'light');
    applyLightTheme();
  } else {
    // Cambiar al tema oscuro
    localStorage.setItem('theme', 'dark');
    applyDarkTheme();
  }
});
// Agregar un manejador de eventos para el evento de actualización de la página
window.addEventListener('beforeunload', () => {
  // Guardar el estado actual del tema en el almacenamiento web
  localStorage.setItem('theme', document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light');
});
// <---------------------------------------------------Fin de Guardar el tema--------------------------------------------------->