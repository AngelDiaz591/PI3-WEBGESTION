/* // Array de colores pasteles
const pastelColors = ["#FFC3A0", "#B2A0E2", "#D9B4A0", "#A0E2E0", "#FFD1B3", "#C8B4E3", "#E6D4A0", "#A0E3D9"];

// Mantener un registro del botón activo
let activeButton = null;

// Función para obtener un color aleatorio de la paleta de colores pasteles
function getRandomPastelColor() {
    const randomIndex = Math.floor(Math.random() * pastelColors.length);
    return pastelColors[randomIndex];
}

// Cambiar el color de fondo y gestionar el botón activo
function handleButtonClick(button) {
    if (activeButton) {
        activeButton.style.backgroundColor = "var(--color-white)"; // Restablecer el color del botón anterior
    }
    const newColor = getRandomPastelColor();
    button.style.backgroundColor = newColor;
    activeButton = button; // Establecer el nuevo botón activo
}

// Agregar un controlador de eventos a cada botón con la clase "colorButton"
const colorButtons = document.querySelectorAll(".colorButton");
colorButtons.forEach(button => {
    button.addEventListener("click", function() {
        handleButtonClick(this);
    });
});

const productCards = document.querySelectorAll(".prod");

// Agrega un evento de clic a cada botón
colorButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        // Oculta todas las tarjetas de productos
        productCards.forEach((card) => {
            card.classList.add("hidden");
        });

        // Muestra la tarjeta de producto correspondiente al botón
        productCards[index].classList.remove("hidden");
    });
}); */

const configurableButtons = document.querySelectorAll(".configurable-button");
const productCards = document.querySelectorAll(".prod");
const scrollableButtons = document.querySelector(".scrollable-buttons");
const leftButton = document.querySelector(".left-button");
const rightButton = document.querySelector(".right-button");

let scrollPosition = 0;

configurableButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        productCards.forEach((card) => {
            card.style.display = "none";
        });
        productCards[index].style.display = "block";
    });

    const bgColor = button.getAttribute("data-bg-color");
    const textColor = button.getAttribute("data-text-color");
    const fontSize = button.getAttribute("data-font-size");

    button.style.backgroundColor = bgColor;
    button.style.color = textColor;
    button.style.fontSize = fontSize + "px";
});

leftButton.addEventListener("click", () => {
    if (scrollPosition > 0) {
        scrollPosition -= 100;
        scrollableButtons.style.transform = `translateX(-${scrollPosition}px)`;
    }
});

rightButton.addEventListener("click", () => {
    if (scrollPosition < scrollableButtons.scrollWidth - scrollableButtons.clientWidth) {
        scrollPosition += 100;
        scrollableButtons.style.transform = `translateX(-${scrollPosition}px)`;
    }
});


