(function () {

    const btnEliminacionProv = document.querySelectorAll(".btnElimiacioProv")

    btnEliminacionProv.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar al proveedor?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el producto?');
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

document.addEventListener("DOMContentLoaded", function() {
    const txtCodigo = document.getElementById("txtCodigo");
    const txtNombre = document.getElementById("txtNombre");
    const NomMarca = document.getElementById("NomMarca");

    NomMarca.addEventListener("input", function() {
        this.value = this.value.toUpperCase();
    });

    txtCodigo.addEventListener("input", function() {
        this.value = this.value.toUpperCase();
    });

    txtNombre.addEventListener("input", function() {
        this.value = this.value.toUpperCase();
    });
});

function mostrarMensajeError(input, mensaje) {
    const errorMessage = input.parentNode.querySelector('.error-message');
    errorMessage.textContent = mensaje;
}

const numPrecioInput = document.getElementById("NumPrecio");
const cantProInput = document.getElementById("CantPro");

function validarNumeroInput(input) {
    const value = parseInt(input.value);
    if (isNaN(value) || value < 1 || value >= 1000000) {
        input.setCustomValidity("Ingrese un número entre 1 <-> 100 000.");
        mostrarMensajeError(input, "Ingrese un número entre 1 <-> 100 000.");
    } else {
        input.setCustomValidity("");
        mostrarMensajeError(input, "");
    }
}

numPrecioInput.addEventListener("input", function() {
    validarNumeroInput(numPrecioInput);
});

cantProInput.addEventListener("input", function() {
    validarNumeroInput(cantProInput);
});

var campos = ['txtCodigo', 'txtNombre', 'NomMarca'];

campos.forEach(function (campoId) {
    var campo = document.getElementById(campoId);

    campo.addEventListener('input', function () {
        var input = this;
        var errorMessage = input.parentNode.querySelector('.error-message');

        if (input.validity.patternMismatch) {
            errorMessage.textContent = 'El nombre debe contener 6 caracteres alfanuméricos';
        } else {
            errorMessage.textContent = '';
        }
    });
});
