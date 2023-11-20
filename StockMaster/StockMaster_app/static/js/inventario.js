(function () {
    const btnEliminacionPro = document.querySelectorAll(".btnEliminacionPro");
    const btnEliminacionProv = document.querySelectorAll(".btnEliminacionProv")
    const btnEliminacionArea = document.querySelectorAll(".btnEliminacionArea");
    const btnEliminacionCate = document.querySelectorAll(".btnEliminacionCate");
    const btnEliminacionMarc = document.querySelectorAll(".btnEliminacionMarc");
    const btnEliminacionRol = document.querySelectorAll(".btnEliminacionRol");
    const btnEliminacionUsua = document.querySelectorAll(".btnEliminacionUsua");

    const btnRecuperarPro = document.querySelectorAll(".btnRecuperarPro");
    const btnRecuperarProv = document.querySelectorAll(".btnRecuperarProv");
    const btnRecuperarArea = document.querySelectorAll(".btnRecuperarArea");
    const btnRecuperarRol = document.querySelectorAll(".btnRecuperarRol");
    const btnRecuperarCate = document.querySelectorAll(".btnRecuperarCate");
    const btnRecuperarMarc = document.querySelectorAll(".btnRecuperarMarc");

    const btnCerrarSesion = document.querySelectorAll(".btnCerrarSesion");

    btnCerrarSesion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea Salir de la página?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionProv.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar al proveedor?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionPro.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el producto?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
    
    btnEliminacionArea.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el area?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionCate.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar la categoria?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionMarc.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar la marca?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionRol.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el rol?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnEliminacionUsua.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea eliminar el usuario?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    //Recuperar

    btnRecuperarPro.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar el producto?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnRecuperarProv.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar al proveedor?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnRecuperarArea.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar al area?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnRecuperarRol.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar el rol?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnRecuperarCate.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar la categoria?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });

    btnRecuperarMarc.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Desea recuperar la marca?');
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
