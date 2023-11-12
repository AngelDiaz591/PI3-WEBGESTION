/* const configurableButtons = document.querySelectorAll(".configurable-button");
const productCards = document.querySelectorAll(".prod");
const scrollContainer = document.querySelector(".scroll-container");
const scrollLeftButton = document.querySelector(".scroll-button.left-button");
const scrollRightButton = document.querySelector(".scroll-button.right-button");

let scrollPosition = 0;

function scrollButtons(direction) {
    const buttonContainerWidth = scrollContainer.clientWidth;
    const buttonWidth = configurableButtons[0].offsetWidth;
    const maxScroll = scrollContainer.scrollWidth - buttonContainerWidth;

    scrollPosition += direction * buttonWidth;
    scrollPosition = Math.max(0, Math.min(scrollPosition, maxScroll));

    scrollContainer.style.transform = `translateX(-${scrollPosition}px)`;
}

scrollLeftButton.addEventListener("click", () => {
    scrollButtons(-1);
});

scrollRightButton.addEventListener("click", () => {
    scrollButtons(1);
});

configurableButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        productCards.forEach((card) => {
            card.style.display = "none";
        });
        productCards[index].style.display = "block";
    });
}); */



/* const configurableButtons = document.querySelectorAll(".configurable-button");
const productCards = document.querySelectorAll(".prod");
const scrollContainer = document.querySelector(".scroll-container");
const scrollLeftButton = document.querySelector(".scroll-button.left-button");
const scrollRightButton = document.querySelector(".scroll-button.right-button");

let scrollPosition = 0;
let selectedButton = null; // Mantener un registro del botón seleccionado

function scrollButtons(direction) {
    const buttonContainerWidth = scrollContainer.clientWidth;
    const buttonWidth = configurableButtons[0].offsetWidth;
    const maxScroll = scrollContainer.scrollWidth - buttonContainerWidth;

    scrollPosition += direction * buttonWidth;
    scrollPosition = Math.max(0, Math.min(scrollPosition, maxScroll));

    scrollContainer.style.transform = `translateX(-${scrollPosition}px}`;
}

function activateButton(button) {
    if (selectedButton) {
        selectedButton.classList.remove("selected");
    }
    button.classList.add("selected");
    selectedButton = button;
}

scrollLeftButton.addEventListener("click", () => {
    scrollButtons(-1);
});

scrollRightButton.addEventListener("click", () => {
    scrollButtons(1);
});

configurableButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        productCards.forEach((card) => {
            card.style.display = "none";
        });
        productCards[index].style.display = "block";
        activateButton(button);
    });
}); */


const configurableButtons = document.querySelectorAll(".configurable-button");
const productCards = document.querySelectorAll(".prod");
const scrollContainer = document.querySelector(".scroll-container");
const scrollLeftButton = document.querySelector(".scroll-button.left-button");
const scrollRightButton = document.querySelector(".scroll-button.right-button");
let scrollPosition = 0;
let selectedButton = null; // Mantén un registro del botón seleccionado

function scrollButtons(direction) {
    const buttonContainerWidth = scrollContainer.clientWidth;
    const buttonWidth = configurableButtons[0].offsetWidth;
    const maxScroll = scrollContainer.scrollWidth - buttonContainerWidth;
    scrollPosition += direction * buttonWidth;
    scrollPosition = Math.max(0, Math.min(scrollPosition, maxScroll));
    scrollContainer.style.transform = `translateX(-${scrollPosition}px)`;
}

function activateButton(button) {
    if (selectedButton) {
        selectedButton.classList.remove("selected");
    }
    button.classList.add("selected");
    selectedButton = button;
}

configurableButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        // Productos relacionados con la categoría seleccionada
        const categoriaId = button.value;
        // Realiza una solicitud a tu servidor para obtener los productos de la categoría
        fetch(`/api/productos?categoriaId=${categoriaId}`)
            .then((response) => response.json())
            .then((data) => {
                // Oculta todos los productos
                productCards.forEach((card) => {
                    card.style.display = "none";
                });
                // Muestra los productos obtenidos
                data.forEach((producto) => {
                    const index = productos.findIndex((p) => p === producto);
                    productCards[index].style.display = "block";
                });
            })
            .catch((error) => {
                console.error("Error al obtener los productos", error);
            });

        scrollButtons(index); // Desplaza el contenedor al botón seleccionado
        activateButton(button); // Activa el botón seleccionado
    });
});

scrollLeftButton.addEventListener("click", () => {
    scrollButtons(-1);
});

scrollRightButton.addEventListener("click", () => {
    scrollButtons(1);
});





