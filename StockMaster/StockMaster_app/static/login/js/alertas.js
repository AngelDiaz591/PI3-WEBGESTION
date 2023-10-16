// Función para eliminar el mensaje al hacer clic en el botón de cerrar
function dismissMessage(button) {
    const messageContainer = button.closest('.alert');
    if (messageContainer) {
        messageContainer.remove();
    }
}