document.addEventListener('DOMContentLoaded', function() {
    // Obtén elementos del DOM
    const showModalButton = document.getElementById("showModal");
    const modal = document.getElementById("myModal");
    const closeModal = document.querySelector(".close");

    // Muestra el modal cuando se hace clic en el enlace
    showModalButton.addEventListener("click", function(event) {
        event.preventDefault(); // Evita el comportamiento predeterminado del enlace
        modal.style.display = "block";
    });

    // Cierra el modal cuando se hace clic en la "x"
    closeModal.addEventListener("click", function() {
        modal.style.display = "none";
    });

    // Cierra el modal si se hace clic fuera del contenido del modal
    window.addEventListener("click", function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});