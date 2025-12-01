document.addEventListener('DOMContentLoaded', function () {
    
    // Función para cerrar todo
    function closeAllMenus() {
        document.querySelectorAll('.modern-context-menu.visible').forEach(menu => {
            menu.classList.remove('visible');
        });
    }

    // 1. Cerrar al hacer clic fuera
    document.addEventListener('click', (e) => closeAllMenus());

    // 2. Cerrar al hacer SCROLL (Importante con position: fixed)
    // Si el usuario hace scroll, el menú se desalinearía, así que mejor lo cerramos.
    window.addEventListener('scroll', () => closeAllMenus(), true);

    const triggers = document.querySelectorAll('.boton-menu-acciones');

    triggers.forEach(trigger => {
        trigger.addEventListener('click', function (e) {
            e.stopPropagation(); // No cerrar inmediatamente
            
            const menu = this.nextElementSibling; // Asumimos que el include está justo después del botón
            const isVisible = menu.classList.contains('visible');

            // Cerrar otros
            closeAllMenus();

            if (isVisible) return; 

            // --- CÁLCULO DE POSICIÓN ---
            // Obtenemos dónde está el botón exactamente en la pantalla
            const rect = trigger.getBoundingClientRect();
            
            // Dimensiones de la ventana
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            
            // Dimensiones del menú (lo hacemos visible invisiblemente para medirlo)
            menu.style.visibility = 'hidden';
            menu.style.display = 'block';
            const menuWidth = menu.offsetWidth;
            const menuHeight = menu.offsetHeight;
            menu.style.display = ''; // Reset
            menu.style.visibility = ''; // Reset

            // 1. Posición Horizontal (Eje X)
            // Intentamos alinear a la izquierda del botón
            let leftPos = rect.left; 
            
            // Si el menú se sale por la derecha (como en tu foto), lo alineamos a la derecha del botón
            if (leftPos + menuWidth > windowWidth) {
                // Lo movemos a la izquierda: Borde derecho del botón - Ancho del menú
                leftPos = rect.right - menuWidth; 
            }
            
            // Aplicamos X
            menu.style.left = `${leftPos}px`;
            menu.style.right = 'auto'; // Limpiamos

            // 2. Posición Vertical (Eje Y)
            const spaceBelow = windowHeight - rect.bottom;
            
            if (menuHeight > spaceBelow) {
                // No cabe abajo -> Mostrar ARRIBA del botón
                menu.style.top = 'auto';
                menu.style.bottom = `${windowHeight - rect.top + 5}px`; // 5px de margen
                menu.style.transformOrigin = 'bottom right'; // Animación desde abajo
            } else {
                // Cabe abajo -> Mostrar ABAJO del botón
                menu.style.top = `${rect.bottom + 5}px`; // 5px de margen
                menu.style.bottom = 'auto';
                menu.style.transformOrigin = 'top right'; // Animación desde arriba
            }

            // --- MOSTRAR ---
            requestAnimationFrame(() => {
                menu.classList.add('visible');
            });
        });
    });
});