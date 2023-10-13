document.addEventListener('DOMContentLoaded', function() {
  const registrationForm = document.getElementById('registrationForm');
  const registerBtn = document.getElementById('registerBtn');

  registrationForm.addEventListener('submit', function(event) {
      // Obtiene todos los campos de entrada requeridos
      const requiredInputs = registrationForm.querySelectorAll('input[required]');

      for (const input of requiredInputs) {
          if (!input.value.trim()) {
              alert('Por favor, completa todos los campos requeridos.');
              event.preventDefault(); // Evita que el formulario se envíe
              return;
          }
      }

      // Si todos los campos requeridos están completos, puedes mostrar el modal aquí
      const modalBtns = document.querySelectorAll('.modalBtn');
      const closeBtn = document.querySelector('.closeIcon');
      const tryAgain = document.querySelector('#okBtn');
      const modal = document.querySelector('.modal');

      modalBtns.forEach(btn => {
          btn.addEventListener('click', () => {
              modal.classList.add('active');
          });
      });

      closeBtn.addEventListener('click', () => {
          modal.classList.remove('active');
      });

      tryAgain.addEventListener('click', () => {
          modal.classList.remove('active');
      });

      window.addEventListener('click', event => {
          if (event.target === modal) {
              modal.classList.remove('active');
          }
      });
  });
});