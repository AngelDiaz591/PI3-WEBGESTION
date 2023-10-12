const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

menuBtn.addEventListener('click', () =>{
    sideMenu.style.display = 'block';
})
closeBtn.addEventListener('click', () =>{
    sideMenu.style.display = 'none';
})
// Add an event listener to the window to listen for the 'resize' event.
window.addEventListener('resize', () =>{
    // If the window width is greater than 768px, show the aside.
    if (window.innerWidth > 768) {
        sideMenu.style.display = 'block';
    }
});

themeToggler.addEventListener('click', () =>{
    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
})


// theme.js

// Función para cambiar el tema
// Función para cambiar el tema y guardar en localStorage
function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-theme-variables')) {
        setTheme('light');
    } else {
        setTheme('dark');
    }
}

// Función para establecer el tema y guardar en localStorage
function setTheme(theme) {
    const body = document.body;
    if (theme === 'dark') {
        body.classList.add('dark-theme-variables');
    } else {
        body.classList.remove('dark-theme-variables');
    }
    localStorage.setItem('theme', theme);
}

// Cargar el tema al inicio
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    setTheme(savedTheme);
}
