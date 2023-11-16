document.addEventListener("DOMContentLoaded", function() {
    var productosContainers = document.querySelectorAll(".mensaje-oculto");
    var noDisponibles = document.querySelectorAll(".no-disponible");

    // Iterar sobre cada contenedor y verificar si hay productos
    productosContainers.forEach(function(container, index) {
        var noDisponible = noDisponibles[index];

        if (container.querySelectorAll('tbody tr').length === 0) {
            // No hay productos, mostrar mensaje de no disponible
            noDisponible.style.display = "block";
        }
    });
});