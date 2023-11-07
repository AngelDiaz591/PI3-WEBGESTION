document.addEventListener("DOMContentLoaded", function () {
    // Obtén la entrada de búsqueda y la lista de productos
    const searchInput = document.getElementById("search-input");
    const products = document.querySelectorAll(".prod"); // Asegúrate de que esta selección sea correcta

    // Guarda el estado original de los elementos product-card
    const originalProductsHTML = Array.from(products).map(product => product.outerHTML).join('');

    // Escucha eventos de cambio en el campo de búsqueda
    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim().toLowerCase();

        products.forEach((product) => {
            const productNameElement = product.querySelector(".product_name");
            const productCategoryElement = product.querySelector("p strong");
            const productName = productNameElement.textContent.toLowerCase();
            const productCategory = productCategoryElement.textContent.toLowerCase();

            const nameMatches = productName.includes(query);
            const categoryMatches = productCategory.includes(query);

            if (nameMatches || categoryMatches) {
                // Muestra el producto si coincide con la búsqueda
                product.style.display = "inline-block"; // Cambiar de "block" a "inline-block"

                // Subraya el texto coincidente en nombre y categoría
                if (nameMatches) {
                    highlightText(productNameElement, query);
                }

                if (categoryMatches) {
                    highlightText(productCategoryElement, query);
                }
            } else {
                // Oculta el producto si no coincide con la búsqueda
                product.style.display = "none";
            }
        });

        if (query === "") {
            // Restablece la lista de productos original cuando se borra el término de búsqueda
            const productList = document.querySelector(".products");
            productList.innerHTML = originalProductsHTML;
            // Establece el estilo display a "inline-block" en el estado original
            const restoredProducts = productList.querySelectorAll(".prod");
            restoredProducts.forEach(product => {
                product.style.display = "inline-block";
            });
        }
    });

    function convertToUppercase() {
        const inputElement = document.getElementById("search-input");
        inputElement.value = inputElement.value.toUpperCase();
    }

    function highlightText(element, query) {
        // Subraya el texto coincidente
        const text = element.textContent;
        const highlightedText = text.replace(
            new RegExp(`(${query})`, "gi"),
            '<span class="highlighted">$1</span>'
        );
        element.innerHTML = highlightedText;
    }
});
