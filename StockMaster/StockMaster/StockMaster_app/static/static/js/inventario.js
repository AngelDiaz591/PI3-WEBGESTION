
(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el producto para siempre? (No se recuperara los datos)');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
})();

// Espera a que se cargue el documento
document.addEventListener("DOMContentLoaded", function () {
    var formulario = document.getElementById('mi_formulario');
    formulario.addEventListener('submit', function (event) {
        var inputImagen = document.getElementById('id_imagen');
        if (inputImagen.files.length === 0) {
            event.preventDefault();
            alert('Por favor, selecciona una imagen antes de enviar el formulario.');
        }
    });
});


