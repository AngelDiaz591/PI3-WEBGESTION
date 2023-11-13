function convertToUppercase() {
  var inputElements = document.querySelectorAll(".campos, .registrar");
  for (var i = 0; i < inputElements.length; i++) {
    inputElements[i].value = inputElements[i].value.toUpperCase();
  }
}
