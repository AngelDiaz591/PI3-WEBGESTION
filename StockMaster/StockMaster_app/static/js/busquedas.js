// Obtén la entrada de búsqueda y la tabla de productos
const searchInput = document.getElementById("search-input");
const productsTable = document.querySelector("table");

// Copia el contenido original de la tabla
const originalTableHTML = productsTable.innerHTML;

// Escucha eventos de cambio en el campo de búsqueda
searchInput.addEventListener("input", function () {
    const query = searchInput.value.trim();
    const rows = productsTable.querySelectorAll("tbody tr");

    rows.forEach((row) => {
        const cells = row.querySelectorAll("td:not(.edita, .elimina)"); // Excluye las celdas de los botones
        let rowMatchesQuery = false;

        cells.forEach((cell) => {
            const text = cell.textContent;
            if (text.toLowerCase().includes(query.toLowerCase())) {
                rowMatchesQuery = true;
                // Divide el texto en partes y agrega la clase a la parte coincidente
                const parts = text.split(new RegExp(`(${query})`, "gi"));
                cell.innerHTML = parts.map(part => {
                    if (part.toLowerCase() === query.toLowerCase()) {
                        return `<span class="highlighted">${part}</span>`;
                    }
                    return part;
                }).join('');
            }
        });

        // Muestra u oculta la fila según si coincide con la búsqueda
        row.style.display = rowMatchesQuery ? "table-row" : "none";
    });

    if (query === "") {
        // Restablece la tabla original cuando se borra el término de búsqueda
        productsTable.innerHTML = originalTableHTML;
    }
});

function convertToUppercase() {
    const inputElement = document.getElementById("search-input");
    inputElement.value = inputElement.value.toUpperCase();
}


