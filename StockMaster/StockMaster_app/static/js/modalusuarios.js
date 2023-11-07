// Agregar un manejador de eventos al botón de cerrar modal (x) y al botón "Cancelar"
document.querySelector(".cerrar").addEventListener("click", function () {
  resetForm();
});

document.querySelector("label[for='btn-modal']").addEventListener("click", function () {
  resetForm();
});

// Función para restablecer el formulario
function resetForm() {
  // Obtén el formulario y sus elementos
  var form = document.querySelector("form");
  var inputs = form.querySelectorAll("input");

  // Recorre los elementos del formulario y restablece sus valores
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].value = "";
  }
}

  // También puedes restablecer los campos de selección y otros elementos si es necesario
  // var selects = form.querySelectorAll("select");
  // for (var i = 0; i < selects.length; i++) {
  //     selects[i].selectedIndex = 0; // Restablecer selecciones a la opción predeterminada
  // }

  // Reinicia el formulario si es necesario
  // form.reset();


var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "flex";
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n);
}

function nextPrev(n) {
  var x = document.getElementsByClassName("tab");
  if (n == 1 && !validateForm()) return false;
  x[currentTab].style.display = "none";
  currentTab = currentTab + n;
  if (currentTab >= x.length) {
    document.getElementById("registrationForm").submit();
    return false;
  }
  showTab(currentTab);
}

function validateForm() {
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  for (i = 0; i < y.length; i++) {
    if (y[i].value == "") {
      y[i].className += " invalid";
      valid = false;
    }
  }
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid;
}

function fixStepIndicator(n) {
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  x[n].className += " active";
}