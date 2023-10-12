function applyDarkTheme() {
    document.body.classList.add('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.add('active');
    themeToggler.querySelector('span:nth-child(2)').classList.remove('active');
  }
  // Función para aplicar el tema claro
  function applyLightTheme() {
    document.body.classList.remove('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.remove('active');
    themeToggler.querySelector('span:nth-child(2)').classList.add('active');
  }
  // Recuperar el estado del tema desde el almacenamiento web
  const savedTheme = localStorage.getItem('theme');
  // Verificar el tema guardado
  if (savedTheme === 'dark') {
    applyDarkTheme();
  } else {
    applyLightTheme();
  }
  // Agregar un manejador de eventos para el botón de cambio de tema
  themeToggler.addEventListener('click', () => {
    if (document.body.classList.contains('dark-theme-variables')) {
      // Cambiar al tema claro
      localStorage.setItem('theme', 'light');
      applyLightTheme();
    } else {
      // Cambiar al tema oscuro
      localStorage.setItem('theme', 'dark');
      applyDarkTheme();
    }
  });
  // Agregar un manejador de eventos para el evento de actualización de la página
  window.addEventListener('beforeunload', () => {
    // Guardar el estado actual del tema en el almacenamiento web
    localStorage.setItem('theme', document.body.classList.contains('dark-theme-variables') ? 'dark' : 'light');
  });
  ​