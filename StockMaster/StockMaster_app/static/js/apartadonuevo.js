/* const categoryCards = document.querySelectorAll('.category-card');
const productCards = document.querySelector('.product-cards');
const categoryContainer = document.querySelector('.category-cards');
const buttonContainer = document.querySelector('.button-container');

// Función para ocultar las category-cards
function hideCategoryCards() {
    categoryContainer.style.display = 'none';
    productCards.style.display = 'block';
    buttonContainer.style.display = 'flex';
    localStorage.setItem('shouldHideCategoryCards', 'true');
}

// Función para mostrar las category-cards
function showCategoryCards() {
    categoryContainer.style.display = 'flex';
    productCards.style.display = 'none';
    buttonContainer.style.display = 'none';
    localStorage.removeItem('shouldHideCategoryCards'); // Elimina el estado local al mostrar las cards
}

// Verifica si las category-cards deben ocultarse según el almacenamiento local
const shouldHideCategoryCards = localStorage.getItem('shouldHideCategoryCards') === 'true';

if (shouldHideCategoryCards) {
    hideCategoryCards();
} else {
    showCategoryCards();
}

categoryCards.forEach((card) => {
    card.addEventListener('click', () => {
        hideCategoryCards();
        // Aquí puedes agregar lógica adicional para filtrar productos por categoría si es necesario.
    });
});

// Verifica si el usuario ha salido de la sección de la página y elimina el estado local
window.addEventListener('beforeunload', () => {
    localStorage.removeItem('shouldHideCategoryCards');
});

// Verifica si el usuario ha ingresado a la sección de la página y muestra las category-cards si corresponde
window.addEventListener('load', () => {
    if (!shouldHideCategoryCards) {
        showCategoryCards();
    }
});*/




const categoryCards = document.querySelectorAll('.category-card');
const productCards = document.querySelector('.product-cards');
const categoryContainer = document.querySelector('.category-cards');
const buttonContainer = document.querySelector('.button-container');

// Función para ocultar las category-cards y el carrusel de botones
function hideCategoryCards() {
    categoryContainer.style.display = 'none';
    productCards.style.display = 'block';
    buttonContainer.style.display = 'flex'; // Oculta el carrusel de botones
    localStorage.setItem('shouldHideCategoryCards', 'true');
}

// Función para mostrar las category-cards y el carrusel de botones
function showCategoryCards() {
    categoryContainer.style.display = 'flex';
    productCards.style.display = 'none';
    buttonContainer.style.display = 'none'; // Oculta el carrusel de botones
    localStorage.removeItem('shouldHideCategoryCards'); // Elimina el estado local al mostrar las cards
}

// Verifica si las category-cards deben ocultarse según el almacenamiento local
const shouldHideCategoryCards = localStorage.getItem('shouldHideCategoryCards') === 'true';

// Verifica si el usuario ha ingresado a la sección de la página y muestra las category-cards si corresponde
window.addEventListener('load', () => {
    if (!shouldHideCategoryCards) {
        showCategoryCards();
    } else {
        hideCategoryCards();
    }
});

categoryCards.forEach((card) => {
    card.addEventListener('click', () => {
        hideCategoryCards();
        // Aquí puedes agregar lógica adicional para filtrar productos por categoría si es necesario.
    });
});

// Verifica si el usuario ha salido de la sección de la página y elimina el estado local
window.addEventListener('beforeunload', () => {
    localStorage.removeItem('shouldHideCategoryCards');
});














//oficial
/* const categoryCards = document.querySelectorAll('.category-card');
const productCards = document.querySelector('.product-cards');
const categoryContainer = document.querySelector('.category-cards');
const buttonContainer = document.querySelector('.button-container');

// Función para ocultar las category-cards y el carrusel de botones
function hideCategoryCards() {
    categoryContainer.style.display = 'none';
    productCards.style.display = 'block';
    buttonContainer.style.display = 'flex'; // Oculta el carrusel de botones
}

// Función para mostrar las category-cards y el carrusel de botones
function showCategoryCards() {
    categoryContainer.style.display = 'flex';
    productCards.style.display = 'none';
    buttonContainer.style.display = 'none'; // Oculta el carrusel de botones
}

// Verifica si el usuario ha ingresado a la sección de la página y muestra las category-cards si corresponde
window.addEventListener('load', () => {
    const hasEnteredSection = localStorage.getItem('hasEnteredSection') === 'true';

    if (hasEnteredSection) {
        showCategoryCards();
    } else {
        hideCategoryCards();
    }
});

categoryCards.forEach((card) => {
    card.addEventListener('click', () => {
        hideCategoryCards();
        // Aquí puedes agregar lógica adicional para filtrar productos por categoría si es necesario.
        localStorage.setItem('hasEnteredSection', 'true'); // Marca que el usuario ha ingresado a la sección
    });
});

// Verifica si el usuario ha salido de la sección de la página y elimina el estado local
window.addEventListener('beforeunload', () => {
    localStorage.removeItem('hasEnteredSection');
}); */




/* const categoryCards = document.querySelectorAll('.category-card');
const productCards = document.querySelector('.product-cards');
const categoryContainer = document.querySelector('.category-cards');
const buttonContainer = document.querySelector('.button-container');

// Función para ocultar las category-cards y el carrusel de botones
function hideCategoryCards() {
    categoryContainer.style.display = 'none';
    productCards.style.display = 'block';
    buttonContainer.style.display = 'none'; // Oculta el carrusel de botones
}

// Función para mostrar las category-cards y el carrusel de botones
function showCategoryCards() {
    categoryContainer.style.display = 'flex';
    productCards.style.display = 'none';
    buttonContainer.style.display = 'none'; // Oculta el carrusel de botones
}

// Verifica si el usuario ha ingresado a la sección de la página y muestra las category-cards si corresponde
window.addEventListener('load', () => {
    const hasEnteredSection = localStorage.getItem('hasEnteredSection') === 'true';

    if (hasEnteredSection) {
        showCategoryCards();
    } else {
        hideCategoryCards();
    }
});

categoryCards.forEach((card) => {
    card.addEventListener('click', () => {
        hideCategoryCards();
        // Aquí puedes agregar lógica adicional para filtrar productos por categoría si es necesario.
        localStorage.setItem('hasEnteredSection', 'true'); // Marca que el usuario ha ingresado a la sección
    });
});

// Verifica si el usuario ha salido de la sección de la página y elimina el estado local
window.addEventListener('beforeunload', () => {
    // Solo elimina el estado local si el usuario ha ingresado a la sección
    if (localStorage.getItem('hasEnteredSection') === 'true') {
        localStorage.removeItem('hasEnteredSection');
    }
}); */

