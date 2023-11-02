document.addEventListener('DOMContentLoaded', function() {
// Obtén todos los elementos con la clase "edit-product-button"
const editButtons = document.querySelectorAll('.edit-product-button');
const editModal = document.getElementById('editModal');
const editProductIdField = document.getElementById('editProductId');

// Obtén todos los elementos con la clase "edit-product-button"
const editButtonsProveedor = document.querySelectorAll('.edit-product-button');
const editModalProveedor = document.getElementById('editModalProveedor');
const editProductIdFieldProveedor = document.getElementById('editProductId');

// Obtén todos los elementos con la clase "edit-product-button"
const editButtonsCategorias = document.querySelectorAll('.edit-product-button-categoria');
const editModalCategoria = document.getElementById('editModalCategoria');
const editProductIdFieldCategorias = document.getElementById('editProductId');

// Obtén todos los elementos con la clase "edit-product-button"
const editButtonsMarcas = document.querySelectorAll('.edit-product-button-marca');
const editModalMarca = document.getElementById('editModalMarca');
const editProductIdFieldMarca = document.getElementById('editProductId');

// Función para abrir el modal de edición Productos
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

// Función para abrir el modal de edición Proveedores
function openEditModalProveedor(productId) {
    editProductIdFieldProveedor.value = productId;

    // Realiza una solicitud Ajax para obtener los detalles del producto y llenar el formulario con esos datos
    // Aquí debes cargar los detalles del producto y llenar el formulario en el modal

    // Abre el modal de edición
    editModalProveedor.style.display = 'flex';
    

    // Obtener el ID del producto y hacer una solicitud AJAX para obtener los detalles
    var productoId = document.getElementById("editProductId").value
    $.ajax({
        url: 'edicionProveedor2/'+ productoId + '',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            $('#EtxtNombre').val(data.nombre)
            $('#EtxtContacto').val(data.contacto)
            $('#EtxtTelefono').val(data.telefono)
            $('#EtxtEmail').val(data.email)
            $('#EtxtCalle').val(data.calle)
            $('#EtxtNoExt').val(data.noExt)
            $('#EtxtNoInt').val(data.noInt)
            $('#EtxtColonia').val(data.colonia)
            $('#EtxtCP').val(data.cp)
            $('#EtxtMunicipio').val(data.municipio)
            $('#EtxtEstado').val(data.estado)
            $('#EtxtPais').val(data.pais)

            if (data.imagen_url) {
                $('#imgActual').attr('src', data.imagen_url);
            }          
        },
        error: function(jqXHR, textStatus, errorThrown){
        }
    });
}

// Función para abrir el modal de edición Categorias 
function openEditModalCategoria(productId) {
    editProductIdFieldCategorias.value = productId;

    // Realiza una solicitud Ajax para obtener los detalles del producto y llenar el formulario con esos datos
    // Aquí debes cargar los detalles del producto y llenar el formulario en el modal

    // Abre el modal de edición
    editModalCategoria.style.display = 'flex';
    

    // Obtener el ID del producto y hacer una solicitud AJAX para obtener los detalles
    var productoId = document.getElementById("editProductId").value
    $.ajax({
        url: 'edicionCategoria2/'+ productoId + '',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            $('#EtxtNombre').val(data.nombre)
        },
        error: function(jqXHR, textStatus, errorThrown){
        }
    });
}

// Función para abrir el modal de edición Marcas 
function openEditModalMarca(productId) {
    editProductIdFieldMarca.value = productId;

    // Realiza una solicitud Ajax para obtener los detalles del producto y llenar el formulario con esos datos
    // Aquí debes cargar los detalles del producto y llenar el formulario en el modal

    // Abre el modal de edición
    editModalMarca.style.display = 'flex';
    
    // Obtener el ID del producto y hacer una solicitud AJAX para obtener los detalles
    var productoId = document.getElementById("editProductId").value
    $.ajax({
        url: 'edicionMarca2/'+ productoId + '',
        type: 'GET',
        dataType: 'json',
        
        success: function (data) {
            console.log(data)
            $('#txtNombre').val(data.nombre)
        },
        error: function(jqXHR, textStatus, errorThrown){
        }
    });
}

// Asigna un evento de clic a cada botón de edición Productos
editButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
        const productId = button.getAttribute('data-id');
        openEditModal(productId);
    });
});

// Asigna un evento de clic a cada botón de edición Proveedores
editButtonsProveedor.forEach(function (button) {
    button.addEventListener('click', function (event) {
        const productId = button.getAttribute('data-id');
        openEditModalProveedor(productId);
    });
});

// Asigna un evento de clic a cada botón de edición Categorias
editButtonsCategorias.forEach(function (button) {
    button.addEventListener('click', function (event) {
        const productId = button.getAttribute('data-id');
        openEditModalCategoria(productId);
    });
});

// Asigna un evento de clic a cada botón de edición Marcas
editButtonsMarcas.forEach(function (button) {
    button.addEventListener('click', function (event) {
        const productId = button.getAttribute('data-id');
        openEditModalMarca(productId);
    });
});
        
});
    

