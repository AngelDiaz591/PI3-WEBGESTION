const configurableButtons = document.querySelectorAll(".configurable-button");
const productCards = document.querySelectorAll(".prod");
const scrollContainer = document.querySelector(".scroll-container");
const scrollLeftButton = document.querySelector(".scroll-button.left-button");
const scrollRightButton = document.querySelector(".scroll-button.right-button");

let scrollPosition = 0;
let selectedButton = null; // Mantener un registro del botón seleccionado

function scrollButtons(event, direction) {

    const buttonContainerWidth = scrollContainer.clientWidth;
    const buttonWidth = configurableButtons[0].offsetWidth;
    const maxScroll = scrollContainer.scrollWidth - buttonContainerWidth;

    scrollPosition += direction * buttonWidth;
    scrollPosition = Math.max(0, Math.min(scrollPosition, maxScroll));

    scrollContainer.style.transform = `translateX(-${scrollPosition}px)`;
}

function activateButton(button) {
    console.log("Botón activado:", button);
    // Desactivar todos los botones
    configurableButtons.forEach((btn) => {
        btn.classList.remove("active");
    });
    // Activar el botón seleccionado
    button.classList.add("active");
}

configurableButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
        activateButton(button); // Activa el botón seleccionado
        scrollButtons(event, 0); // Llama a scrollButtons con dirección 0
        // Tu código adicional aquí para responder al clic del botón
    });
});








