document.addEventListener('DOMContentLoaded', function() {
// Obtén todos los elementos con la clase "edit-product-button"
const editButtons = document.querySelectorAll('.edit-product-button');
const editModal = document.getElementById('editModal');
const editProductIdField = document.getElementById('editProductId');

// Función para abrir el modal de edición
function openEditModal(productId) {
    editProductIdField.value = productId;

    // Realiza una solicitud Ajax para obtener los detalles del producto y llenar el formulario con esos datos
    // Aquí debes cargar los detalles del producto y llenar el formulario en el modal

    // Abre el modal de edición
    editModal.style.display = 'flex';
    

    // Obtener el ID del producto y hacer una solicitud AJAX para obtener los detalles
    var productoId = document.getElementById("editProductId").value
    var proveedorOp = document.querySelectorAll(".proveedorOp")
    var categroiaOp = document.querySelectorAll(".categoriaOp")
    var marcaOP = document.querySelectorAll(".marcaOP")
    $.ajax({
        url: 'edicioninventario2/'+ productoId + '',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            $('#EtxtCodigo').val(data.codigo)
            $('#EtxtNombre').val(data.nombre)
            $('#ENumPrecio').val(data.precio)
            $('#ECantPro').val(data.cantPro)
            if (data.imagen_url) {
            $('#imgActual').attr('src', data.imagen_url);
        }          
            for (var i = 0; i < proveedorOp.length; i++) {
                var option = proveedorOp[i];
            if (option.value == data.id_Proveedores) {
            $(option).prop('selected', true);
            break;  // Terminar el bucle después de encontrar la coincidencia
            }
        }
            for (var i = 0; i < categroiaOp.length; i++) {
                        var option = categroiaOp[i];
                    if (option.value == data.id_categorias) {
                    $(option).prop('selected', true);
                    break;  // Terminar el bucle después de encontrar la coincidencia
                }
            }

            for (var i = 0; i < marcaOP.length; i++) {
                        var option = marcaOP[i];
                    if (option.value == data.id_marca) {
                    $(option).prop('selected', true);
                    break;  // Terminar el bucle después de encontrar la coincidencia
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
        }
    });
}
// Asigna un evento de clic a cada botón de edición
editButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
        const productId = button.getAttribute('data-id');
        openEditModal(productId);
    });
});

// Resto del código para cerrar el modal y otros eventos

    // Cierra el modal de edición cuando se hace clic en la "x"
    closeEditModal.addEventListener("click", function() {
        editModal.style.display = "none";
    });
    
    //Cierra el modal de edicion cuando se da click a cancelar
    cancelar.addEventListener("click", function() {
        editModal.style.display = "none";
    });

    // Cierra el modal de edición si se hace clic fuera del contenido del modal
    window.addEventListener("click", function(event) {
        if (event.target === editModal) {
            editModal.style.display = "none";
        }
    });

    
});

