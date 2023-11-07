document.addEventListener('DOMContentLoaded', function() {
    const submenuTriggers = document.querySelectorAll('.submenu-trigger');
    const mainMenuLinks = document.querySelectorAll('.main-menu-link');

    // Recuperar el estado de los submenús al cargar la página
    submenuTriggers.forEach(trigger => {
        const submenuContainer = trigger.nextElementSibling;
        const storedState = sessionStorage.getItem(`submenuState_${trigger.dataset.submenuId}`);

        if (storedState === 'open') {
            openSubmenu(submenuContainer);
        } else {
            closeSubmenu(submenuContainer);
        }

        trigger.addEventListener('click', function(event) {
            event.preventDefault();
            const submenuContainer = this.nextElementSibling;
            toggleSubmenu(submenuContainer);
        });
    });

    mainMenuLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            const submenuContainer = link.nextElementSibling;
            if (submenuContainer && submenuContainer.classList.contains('submenu-container')) {
                closeSubmenu(submenuContainer);
            }
        });
    });

    function toggleSubmenu(submenuContainer) {
        if (submenuContainer.style.display === 'block' || getComputedStyle(submenuContainer).display === 'block') {
            closeSubmenu(submenuContainer);
        } else {
            openSubmenu(submenuContainer);
            closeOtherSubmenus(submenuContainer);
            storeSubmenuState(submenuContainer);
        }
    }

    function openSubmenu(submenuContainer) {
        submenuContainer.style.display = 'block';
        const trigger = submenuContainer.previousElementSibling;
        sessionStorage.setItem(`submenuState_${trigger.dataset.submenuId}`, 'open');
    }

    function closeSubmenu(submenuContainer) {
        submenuContainer.style.display = 'none';
        const trigger = submenuContainer.previousElementSibling;
        sessionStorage.setItem(`submenuState_${trigger.dataset.submenuId}`, 'closed');
    }

    function closeOtherSubmenus(currentSubmenuContainer) {
        const allSubmenuContainers = document.querySelectorAll('.submenu-container');
        allSubmenuContainers.forEach(submenuContainer => {
            if (submenuContainer !== currentSubmenuContainer) {
                closeSubmenu(submenuContainer);
            }
        });
    }

    function storeSubmenuState(submenuContainer) {
        const trigger = submenuContainer.previousElementSibling;
        sessionStorage.setItem(`submenuState_${trigger.dataset.submenuId}`, 'open');
    }
});

window.addEventListener('beforeunload', function(event) {
    // Borrar el estado de los submenús al recargar la página
    submenuTriggers.forEach(trigger => {
        const submenuContainer = trigger.nextElementSibling;
        storeSubmenuState(submenuContainer);
    });
});